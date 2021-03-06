//demostración del uso de queues con FreeRTOS
#include <Arduino_FreeRTOS.h>
#include "queue.h"

//macros para la configuración y manejo de pines
#define MakeInputPin(REG, PIN)       (REG &= (~(1 << PIN)))
#define MakeOutputPin(REG, PIN)      (REG |= (1 << PIN))
#define EnablePullUp(REG, PIN)       (REG |= (1 << PIN))
#define ReadInputPin(REG, PIN)       (REG & (1 << PIN))
#define WriteOutputPinLow(REG, PIN)  (REG &= ~(1 << PIN))
#define WriteOutputPinHigh(REG, PIN) (REG |= (1 << PIN))
#define ToggleOutputPin(REG, PIN)    (REG ^= (1 << PIN))

//declaraciones de la tasa de comunicación serial
#define F_CPU 16000000UL
#define USART_BAUDRATE 19200
#define UBRR_VALUE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)

const TickType_t xTicksToWait = pdMS_TO_TICKS(100);

//handle para un queue
QueueHandle_t myQueue;

//buffer para el UART
unsigned char mybuffer[25];

//Tecla presionada
//Modificada por el isr
int row = 0;
char* teclas[] = {"*0#D", "789C", "456B", "123A"};

void setup()
{
  //Forzar para crear queue, debe ser creada antes de usarla por xTask
  while(true){
    //Tamaño de queue pequeño para limitar datos en caso de un rebote
    myQueue = xQueueCreate(3, sizeof(int32_t));
    //revisa si la queue ha sido creada
    if(myQueue != NULL)
    {
      break;
    }
  }

  //creación de tareas
  xTaskCreate(vSenderRows,       "ROWS SENDER",   100, NULL, 1, NULL);
  xTaskCreate(vReceiverTask,     "RECEIVER TASK", 100, NULL, 1, NULL);

  // Renglones en alta impedancia
  MakeInputPin(DDRB, PB3); WriteOutputPinHigh(PORTB, PB3);
  MakeInputPin(DDRB, PB2); WriteOutputPinHigh(PORTB, PB2);
  MakeInputPin(DDRB, PB1); WriteOutputPinHigh(PORTB, PB1);
  MakeInputPin(DDRB, PB0); WriteOutputPinHigh(PORTB, PB0);

  // Columnas en pullup
  MakeInputPin(DDRD, PD7); EnablePullUp(PORTD, PD7);
  MakeInputPin(DDRD, PD6); EnablePullUp(PORTD, PD6);
  MakeInputPin(DDRD, PD5); EnablePullUp(PORTD, PD5);
  MakeInputPin(DDRD, PD4); EnablePullUp(PORTD, PD4);

  //interrupciones para DDRD
  //se habilita interrupción por cambio de estado en PORTD
  PCICR |= (1 << PCIE2);
  PCMSK2 |= (1<<7)|(1<<6)|(1<<5)|(1<<4);
  sei();

  //configuración del puerto serial
  UBRR0H = (uint8_t)(UBRR_VALUE >> 8);
  UBRR0L = (uint8_t)UBRR_VALUE;
  UCSR0C = 0x06;       // Set frame format: 8data, 1stop bit
  UCSR0B |= (1 << RXEN0) | (1 << TXEN0);   // TX y RX habilitados
}

void vSenderRows(void * pvParameters){
  while(true){
    MakeOutputPin(DDRB, row);
    WriteOutputPinLow(PORTB, row);
    //Delay de 60ms, debido a la lectura de posibles rebotes en teclado que duren hasta 50 ms, el doble de un rebote normal
    _delay_ms(60);
    WriteOutputPinHigh(PORTB, row);
    MakeInputPin(DDRB, row);
    row = (row + 1) % 4;
  }
}

void vReceiverTask(void * pvParameters)
{
  char valueReceived;
  BaseType_t qStatus;
  while(1)
  {
    qStatus = xQueueReceiveFromISR(myQueue, &valueReceived, xTicksToWait);
    if(qStatus == pdPASS)
    {
      sprintf(mybuffer, "%c", valueReceived);
      USART_Transmit_String((unsigned char *)mybuffer);
    }
    vTaskDelay(pdMS_TO_TICKS(250));
  }
}

//////////funciones de transmisión del UART///////////////

void USART_Transmit(unsigned char data)
{
  while(!(UCSR0A & (1 << UDRE0)));
  UDR0 = data;
}

void USART_Transmit_String(unsigned char * pdata)
{
  unsigned char i;
  unsigned char len = strlen(pdata);
  for(i=0; i < len; i++)
  {
    while(!(UCSR0A & (1 << UDRE0)));
    UDR0 = pdata[i];
  }
}

//////////////////////////////////////////////////////////////

ISR(PCINT2_vect){
  int pin_interrupt[4] = {7, 6, 5, 4};
  int row_interrupt = row;
  for(int i=0; i<4; i++){
    if(ReadInputPin(PIND, pin_interrupt[i]) == 0)
    {
      _delay_ms(25);
      while(ReadInputPin(PIND, pin_interrupt[i]) == 0);
      char key = teclas[row_interrupt][i];
      xQueueSendToBackFromISR(myQueue, &key, xTicksToWait);
      return;
    }
  }
}


void loop() {

}
