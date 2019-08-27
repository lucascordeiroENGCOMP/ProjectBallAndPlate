

// ajustar os parametros do PID  até encontrar os valores otimos

#define   kp        2.5      //constante de ganho proporcional
#define   ki        1.0      //constante de ganho integral (o valor m�nimo de Ki deve ser tal que ki*acc_max >= 1023)
#define   kd        0.05     //constante de ganho derivativo

// ajustar os valores em graus 0 a 180
// 90 + 45 e 90 - 45

#define   acc_max   1023     //valor m�ximo para o acumulador de erro
#define   acc_min   -1023    //valor m�nimo para o acumulador de erro

// setpoint posição de equilibrio
// lembrar o que pid que vamos usar  é bidimensional
// pid para o x e pid para o y
// usar o codigo duas vezes (lembrar)
 
int setpoint=0;           //valor desejado da velocidade do motor (em pulsos do encoder)

int erro_anterior=0;      //erro anterior entre setpoint e valor medido (usado no c�lculo do termo derivativo)

int integral=0;           //acumulador do erro (usado no c�lculo do termo integral)



//declara��o da fun��o de controle

// nosso PID terá que ser um pid bidimensional
// só que a resposta do pid bi, deve atuar em um sistema que tem 3 graus de liberdade ( os 3 servos motores )

int PID(int setpoint, int vel_atual)
{   
   int erro;                                  //declara o erro
   int derivativo;                            //declara o termo derivativo
   float pid_output;                          //sa�da do controlador PID com o valor do PWM a ser enviado aos motores
  
   erro = setpoint-vel_atual;                 //define o erro atual
   
   integral = integral + erro;                //soma o valor do erro ao valor da integral
   if(integral > acc_max)                     //limita o valor da integral ao valor m�ximo permitido(acc_max)
   {                        
    integral = acc_max;
   }
   else if(integral < acc_min)                //limita o valor da integral ao valor m�nimo permitido(acc_min)
   {                    
    integral = acc_min;
   }
   
   derivativo = erro-erro_anterior;              //define a varia��o do erro como a diferen�a entre a erro atual e o erro anterior
   erro_anterior = erro;                         //atualiza o valor do erro anterior
   
   // caluculo do PID 
   pid_output = (kp * (float)erro) + (ki * (float)integral) + (kd * (float)derivativo);   //define a sa�da do controle PID como a soma dos termos proporcional, integral e derivativo
   
   // setar para  180 graus por exemplo
   
   if(pid_output > 1023)          //pro�be que o sinal PWM seja maior que 1023 (valor m�ximo permitido)
   {
    pid_output = 1023;                           
   }
   else if(pid_output < -1023)   //pro�be que o sinal PWM seja menor que -1023 (valor m�nimo permitido)
   {
    pid_output = -1023;                          
   }

   return pid_output;
}


//modo de utiliza��o da fun��o de controle
PID(setpoint, grandeza_atual)
