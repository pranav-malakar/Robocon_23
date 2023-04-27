//Methods tried and reasons they failed:-
//1)Task resume and suspend: Many extra tasks have to be created and arduino uno is not able to execute more than 5 tasks
//2)Message Queues: There was too much random delay experienced while executing the tasks
//3)Mutex: too much delay was experienced while taking input from controller and it was randomly stopping
//4)semaphore: Was able to run only one task at a time
//Task suspend and Resume code
#include <Arduino_FreeRTOS.h>      //Free RTOS library
#include <PS2X_lib.h>              //PS2 library

//creating a constant variable for the led
#define led1 8
#define led2 7

//TaskHandle_t Type by which tasks are referenced.
TaskHandle_t TaskHandle_1;
TaskHandle_t TaskHandle_2;
TaskHandle_t TaskHandle_3;
TaskHandle_t TaskHandle_4;

PS2X ps2x;                         //object creation

int error = 0;

//creating task functions
void TaskBlink1( void *pvParameters );
void TaskBlink2( void *pvParameters );
void Taskinput( void *pvParameters );
void Taskorder( void *pvParameters );

void setup()
{
  Serial.begin(9600);
  //Creating 4 tasks
  //Task Creation Syntax:-
  //  BaseType_t xTaskCreate( TaskFunction_t pvTaskCode,
  //                          const char * const pcName,
  //                          configSTACK_DEPTH_TYPE usStackDepth,
  //                          void *pvParameters,
  //                          UBaseType_t uxPriority,
  //                          TaskHandle_t *pxCreatedTask );
  xTaskCreate(TaskBlink1, "task1", 128, NULL, 1, &TaskHandle_1 );  //Creating Task1 with priority 1 where 1 has the least priority
  xTaskCreate(TaskBlink2, "task2", 128, NULL, 1, &TaskHandle_2 );  //Creating Task2 with priority 1 where 1 has the least priority
  xTaskCreate(Taskinput, "task3", 128, NULL, 1, &TaskHandle_3 );   //Creating Task3 with priority 1 where 1 has the least priority
  xTaskCreate(Taskorder, "task4", 128, NULL, 2, &TaskHandle_4);    //Creating Task4 with priority 1 where 1 has the least priority

  vTaskStartScheduler();
}

void loop()
{
  //There is no instruction in the loop section of the code.
  // Because each task executes on interrupt after specified time
}

void TaskBlink1(void *pvParameters)       //Task 1 to keep the led1 on
{
  Serial.println("Inside Task1");
  pinMode(led1, OUTPUT);
  digitalWrite(led1, HIGH);
  vTaskResume(TaskHandle_4);             //Resuming task4
}

void TaskBlink2(void *pvParameters)       //Task2 to turn on the led2 for 5 seconds and the stop it
{
  Serial.println("Inside Task2");
  pinMode(led2, OUTPUT);
  digitalWrite(led2, HIGH);
  vTaskDelay(5000 / portTICK_PERIOD_MS);
  digitalWrite(led2, LOW);
  vTaskResume(TaskHandle_4);                //Resuming task4
}

void Taskinput(void *pvParameters)         //Task3 to get the input from ps2 controller 
{
  while (1)
  {
    error = ps2x.config_gamepad(13, 11, 10, 12, true, true);
    ps2x.read_gamepad();          //read controller
    if (ps2x.Button(PSB_PAD_UP)) //will be TRUE as long as button is pressed
    {
      Serial.println("Up ");
      Serial.println("Task1");
      vTaskResume(TaskHandle_1);//Resuming task1 when the up button is pressed
    }
    if (ps2x.Button(ORANGE_FRET)) // print stick value IF TRUE
    {
      Serial.println("Cross symbol");
      Serial.println("Task2");
      vTaskResume(TaskHandle_2);//Resuming task2 when the cross symbol button is pressed
    }
  }
}

void Taskorder(void *pvParameters)           //Task4 to execute the tasks in order
{
  while (1)
  {
    Serial.println(F("Task4 Running, Suspending all tasks"));
    digitalWrite(led1, LOW);
    vTaskSuspend(TaskHandle_1);    //Suspend Task1
    digitalWrite(led2, LOW);
    vTaskSuspend(TaskHandle_2);    //Suspend Task2
    vTaskSuspend(NULL);            //Suspend Task4
    //All tasks except task3 are suspended so the task 3 will run
  }
}
