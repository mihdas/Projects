// ASSIGNMENT SUBMITTED BY MEGHA AGARWAL(1810110129) AND MIHIR VIPRADAS(1810110130)
#include <stdio.h>//printf,perror,getchar()
#include <unistd.h>//chdir(),fork(),exec(),pid_t
#include <stdlib.h>//malloc(),exit(),free()
#include <string.h>//strcmp(),strok()

#define MAX_LINE 80 /* The maximum length of a command */
#define BUFFER_SIZE 50
#define buffer "\n Command History:\n"

//declarations
char history[10][BUFFER_SIZE]; //history array to store history commands
int count = 0;

void History() //function to display the history of commands
{

  printf("Command history:\n");
  int i;int j = 0;
  int histCount = count;

  //loop for iterating through commands
  for (i = 0; i<10;i++)
  {
    //command index
    printf("%d.  ", histCount);
    while (history[i][j] != '\n' && history[i][j] != '\0')
    {
      //printing command
      printf("%c", history[i][j]);
      j++;
    }
    printf("\n");
    j = 0; //resets the arg for the next instrunxion
    histCount--;
    if (histCount ==  0)
    break;
  }
}

//char *args declares a pointer array to point to a constant array

//Funxion to get the command from shell, tokenize it and set the args parameter
int formatCommand(char inputBuffer[], char *args[],int *flag)
{
  int length; // # of chars in command line
  int i;     // loop index for inputBuffer
  int start = -1;  // index of beginning of next command
  int nx = 0; // index of where to place the next parameter into args[]
  int hist;
  //read user input on command line and checking whether the command is !! or !n

  length = read(STDIN_FILENO, inputBuffer, MAX_LINE);//calculates the length of the command

  if (length == 0) //nothing has been entered
  {
    exit(0);   //end of command
  }
  if (length < 0) //some error
  {
    printf("Command not read\n");
    exit(-1);  //terminate
  }
  //examine each character
  for ( i=0 ; i < length ; i++ )
  {
    switch (inputBuffer[i])
    {
      case ' '://to prevent a whitespace from going into the default section
      case '\t' : // to seperate arguments
      if(start != -1)
      {
        args[nx] = &inputBuffer[start];
        nx++;
      }
      inputBuffer[i] = '\0'; // add a null character at the end
      start = -1;
      break;

      case '\n'://final char
      if (start != -1)
      {
        args[nx] = &inputBuffer[start];
        nx++;
      }
      inputBuffer[i] = '\0';
      args[nx] = NULL; // no more args
      break;

      default :
      if (start == -1)
      start = i;
      if (inputBuffer[i] == '&') // check if the user wants the child to run in the background
      {
        *flag  = 1; //this flag is the differentiate whether the parent will wait or not
        inputBuffer[i] = '\0';
      }
    }
  }

  args[nx] = NULL; //if the input line was > 80

  if(strcmp(args[0],"history")==0) //if the two strings are the same it returns a zero
  {
    if(count>0)
    {
      History();
    }
    else
    {
      printf("\n No Commands in the history \n");
    }
    return -1;
  }
  if(strcmp(args[0],"quit") == 0)//exits the shell
  {
    printf("Thank you for using my shell\n");
    exit(0);//terminates the shell
  }
  if(strcmp(args[0],"help")== 0)//displays help
  {
    printf("You can do the following things in this shell\n");
    printf("1.Execute all the builtin functions\n");
    printf("2.Type history to get a list of the last 10 commands entered\n");
    printf("3.You can enter & at the end of your file to run it in the background\n");
    printf("4.You can enter !! to execute the most recent command\n5.You can enter nters a single ! followed by an integer N ,the Nth command in the history will be executed ");
    printf("\n6.Enter quit to exit\n");
    return -1;//returns to ask for the next command
  }

  if (args[0][0]-'!' == 0) //comparing ASCII values for !
  {
    int x = args[0][1]- '0'; //ASCII value of 0=48
    int y = args[0][2]- '0';

    if(x > count) //second letter check
    {
      printf("\nNo Such Command in the history\n");
      strcpy(inputBuffer,"Wrong command");
    }
    else if (y != -48) //third letter check
    {
      printf("\nNo such command in the history. Enter <=!9 (buffer size is 10 along with current command)\n");
      strcpy(inputBuffer,"Wrong command");
    }
    else
    {
      if(x==-15)//Checking for '!!',ascii value of '!' is 33.
      {
        strcpy(inputBuffer,history[0]);  // this will be your (last) command
      }
      else if(x==0) //Checking for '!0'
      {
        printf("Enter proper command");
        strcpy(inputBuffer,"Wrong command");
      }

      else if(x>=1) //Checking for '!n', n >=1
      {
        //printf("count is %d\n",count);
        strcpy(inputBuffer,history[count-x]);
    }
  }
}
for (i = 9;i>0; i--) //Moving the history elements one step higher
strcpy(history[i], history[i-1]);
strcpy(history[0],inputBuffer); //Updating the history array with input buffer
count++;
if(count>10)
{
  count=10;
}
}

int main(void)
{
  char inputBuffer[MAX_LINE]; /* buffer to hold the input command */
  int flag; // equals 1 if a command is followed by "&"
  char *args[MAX_LINE/2 + 1];/* max arguments */

  pid_t pid,tpid;
  int i;
  printf("\n**** OPERATING SYSTEMS ASSIGNMENT****");
  printf("\nMADE BY MEGHA AGARWAL 1810110129 , MIHIR VIPRADAS 1810110130");
  char* username = getenv("USER");
  printf("\nEnter help for furthur instructions\nUSER is: @%s\n", username);

  while (1) //infinite loop for shell prompt
  {
    flag = 0; //flag =0 by default

    printf("osh>");
    fflush(stdout);
    if(formatCommand(inputBuffer,args,&flag)!=-1) // get next command
    {
      pid = fork();//obtain the process id
      if (pid < 0)//if pid is less than 0, forking fails
      {
        printf("Fork failed.\n");
        exit (1);
      }
      if (pid == 0)//if pid ==0
      {  	 	//command not executed
        printf("--- Child  ---\nCurrent PID: %d and Child PID: %d\n",getpid(), pid);
        if (execvp(args[0], args) == -1)
        {
          printf("Error executing command\n");
        }

      }
      if(pid > 0)//forking has been successful
      {
        i++;
        printf("---Parent ---\nCurrent PID: %d and Child PID: %d\n",getpid(),pid);
        if (flag == 0)// if flag == 0, the parent will wait, otherwise returns to the formatCommand() funnxion.
        {
          i++;
          wait(NULL);//wait till any child process is completed,in this we will only have a single child hence this command is the most efficient
        }
      }
    }
  }
}
// The child process will take the first if condition (where pid == 0).
//In the child process, we want to run the command given by the user. So, we use one of the many variants of the exec system call, execvp. The different variants of exec do slightly different things. Some take a variable number of string arguments. Others take a list of strings. Still others let you specify the environment that the process runs with. This particular variant expenxs a program name and an array (also called a venxor, hence the ‘v’) of string arguments (the first one has to be the program name). The ‘p’ means that instead of providing the full file path of the program to run, we’re going to give its name, and let the operating system search for the program in the path.
//If the exec command returns -1 (or anxually, if it returns at all), we know there was an error. So, we use printf to print the system’s error message,Then, we exit so that the shell can keep running.
