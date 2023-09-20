//Public Domain by CodeMonkey1100001001 2016.05.06

char incomingData[256];//incoming serial commands
int  incomingDataPointer=0x00;
int  incomingDataSize=256;
byte ATCommandReady=0x00;

//these must always stay in order 
//they are used in a swtich case below
#define ATCommandCount 5
char *ATCommands[ATCommandCount] = {
"+HELO", //0
"+RAND", //1
"+NULL", //2
"+STAT", //3 note if two similar commands match the longer one must come first
"+STA"   //4
};

byte incomingByte=0x00;

void setup() 
{
  Serial.begin(9600);
  delay(2000);while(!Serial);//delay for Leonardo
  Serial.println("AT Command Receiver");
  Serial.println("Version 2016/05/06 0.000");
  Serial.println("OK");
  
}

void loop() 
{
  if (Serial.available() >0)
  {
    incomingByte=Serial.read();
    incomingByte=toupper(incomingByte); // case insenstive always upper case
    if (incomingByte=='\n') ATCommandReady=1;
    incomingData[incomingDataPointer]=incomingByte;
    incomingDataPointer++;
    if (incomingDataPointer>=incomingDataSize) incomingDataPointer=incomingDataSize-1;
  }
  if (ATCommandReady==1)
  {
    int success=parseATCommand();
    incomingDataPointer=0;
    ATCommandReady=0;
    if (success==1) Serial.println("OK");
    else Serial.println("ERROR");
  }

}//loop


int parseATCommand()
{
  int retV=-1;
  int ATCommandMatched=0;
  int parsePointer=0x00;

    //The first 2 chars of the incoming data must be AT
    if ( strncmp(incomingData,"AT",2)==0 ) 
    {
       //is it just an AT\r\n
      if (incomingData[2]=='\r' || incomingData[2]=='\n') ATCommandMatched=1;
      retV=1;//just return OK
      parsePointer=2; // skip the AT
      
      for (int lop=0; lop< ATCommandCount; lop++)//loop over all the known commands
      {
        int returnVal=compareCommand(ATCommands[lop],incomingData,parsePointer,strlen(ATCommands[lop]));
        if (returnVal==1) 
        { 
          ATCommandMatched=1;
          parsePointer=parsePointer+strlen(ATCommands[lop]);
          int getSet=0;// 0=get 1=set
          if (incomingData[parsePointer]=='=') getSet=1;//this will effectively ignore ? if present
          parsePointer++;
          
          switch (lop)
          {
            case 0:
              //+HELO
              //retV=atCommand_CCLK(getSet,parsePointer,incomingDataPointer);
              Serial.println("Hello AT Reader");
              break;
            case 1:
              //+RAND
              retV=ATCommand_RAND(getSet,parsePointer,incomingDataPointer);
              break;
            case 2:
              //+NULL
              //do nothing
              break;
            case 3:
              //+STAT
              Serial.println("+STATUS=A OK!");
              break;
            case 4:
              //+STA
              //abbreviated status
              Serial.println("A OK!");
              break;
          }//switch
          lop=ATCommandCount;
          //retV=1;// OK or ERROR
        }//if returnVal==1
        
       }//match a command;
       if (ATCommandMatched==0) { Serial.println("No command match"); retV=-1;}
    }//was at matched
  return retV;
}//parseATCommand()

int ATCommand_RAND(int getSet,int startPtr, int endPtr)
{
  int retV=1;
  int validData=0;
  String inString="";  
  int maxVal=10;
  if (getSet==1)//set
  {
    for(int i=startPtr; i<endPtr; i++)
    {
      
      inString += (char)incomingData[i];
      
      if (incomingData[i] == '\n') 
      {
        maxVal=inString.toInt();
      }
    }
  }
  Serial.print("Generating Random Value from 0 to ");
  Serial.println(maxVal);

  Serial.print("+RAND=");
  Serial.println(random(0,maxVal),DEC);
  return retV;
}//ATCommand_RAND

int compareCommand(char *needle, char *haystack,int startPos, int compareLen)
{
  int retV=0;
  
  for (int i=0; i< compareLen; i++)
  {
    //Serial.print("needle="); Serial.print(needle[i]);
    //Serial.print(" hay="); Serial.print(haystack[i+startPos]);
    //Serial.println("");
    if (needle[i]==haystack[i+startPos]) retV++;
  }
  
  //Serial.println("-=--");
  
  if (compareLen==retV) retV=1;
    else retV=0;
  
  return retV;
}
