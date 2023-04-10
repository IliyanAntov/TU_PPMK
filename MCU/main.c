#include <stdio.h>
#include <driverlib.h>
#include <math.h>
#include "grlib.h"
#include "Crystalfontz128x128_ST7735.h"
#include "uartstdio.h"

#define MAX_STR_SIZE	20

volatile char score[20] = {"0000000"};
volatile int score_changed = 0;

/* Graphic library context */
Graphics_Context g_sContext;
Graphics_Rectangle score_text_box;


void init_clock_system(void)
{
    CS_setDCOFreq(CS_DCORSEL_1, CS_DCOFSEL_4); //DCO = 16 MHz
    CS_initClockSignal(CS_SMCLK, CS_DCOCLK_SELECT, CS_CLOCK_DIVIDER_1); //SMCLK = DCO clock
}

void init_lcd(void)
{
    Crystalfontz128x128_Init(); // Initializes display driver
    Crystalfontz128x128_SetOrientation(LCD_ORIENTATION_UP); // Set default screen orientation
    Graphics_initContext(&g_sContext, &g_sCrystalfontz128x128); // Initializes graphics context
    Graphics_setForegroundColor(&g_sContext, GRAPHICS_COLOR_WHITE);
    Graphics_setBackgroundColor(&g_sContext, GRAPHICS_COLOR_BLACK);
    GrContextFontSet(&g_sContext, &g_sFontFixed6x8);
    Graphics_clearDisplay(&g_sContext);

    score_text_box.xMin = 0;
    score_text_box.xMax = 128;
    score_text_box.yMin = floor(60 - ((float)Graphics_getStringHeight(&g_sContext) / 2));
    score_text_box.yMax = ceil(60 + ((float)Graphics_getStringHeight(&g_sContext) / 2));
}


void init(void)
{
    // Stop watchdog timer
    WDT_A_hold(WDT_A_BASE);
    // Disable the GPIO power-on default high-impedance mode
    // to activate previously configured port settings
    PMM_unlockLPM5();

    FRAMCtl_configureWaitStateControl(FRAMCTL_ACCESS_TIME_CYCLES_1); //Needed for DCO = 16 MHz

    init_clock_system();


    // -----custom code-----

    // ----------------------- ADC initialization start -----------------------

    // Joystick X analog pin
    GPIO_setAsInputPin(GPIO_PORT_P9, GPIO_PIN2);
    GPIO_setAsPeripheralModuleFunctionInputPin(GPIO_PORT_P9, GPIO_PIN2, GPIO_TERNARY_MODULE_FUNCTION);
    // Joystick Y analog pin
    GPIO_setAsInputPin(GPIO_PORT_P8, GPIO_PIN7);
    GPIO_setAsPeripheralModuleFunctionInputPin(GPIO_PORT_P8, GPIO_PIN7, GPIO_TERNARY_MODULE_FUNCTION);


    ADC12_B_initParam adc_init_struct;
    adc_init_struct.sampleHoldSignalSourceSelect = ADC12_B_SAMPLEHOLDSOURCE_SC;
    adc_init_struct.clockSourceSelect = ADC12_B_CLOCKSOURCE_SMCLK;
    adc_init_struct.clockSourceDivider = ADC12_B_CLOCKDIVIDER_1;
    adc_init_struct.clockSourcePredivider = ADC12_B_CLOCKPREDIVIDER__1;
    adc_init_struct.internalChannelMap = ADC12_B_MAPINTCH0;
    ADC12_B_init(ADC12_B_BASE, &adc_init_struct);

    ADC12_B_enable(ADC12_B_BASE);

    ADC12_B_setupSamplingTimer(ADC12_B_BASE,
                               ADC12_B_CYCLEHOLD_16_CYCLES,
                               ADC12_B_CYCLEHOLD_4_CYCLES,
                               ADC12_B_MULTIPLESAMPLESENABLE);


    ADC12_B_configureMemoryParam XMemoryParam = {0};
    XMemoryParam.memoryBufferControlIndex = ADC12_B_MEMORY_0;
    XMemoryParam.inputSourceSelect = ADC12_B_INPUT_A10;
    XMemoryParam.refVoltageSourceSelect = ADC12_B_VREFPOS_AVCC_VREFNEG_VSS;
    XMemoryParam.endOfSequence = ADC12_B_NOTENDOFSEQUENCE;
    XMemoryParam.windowComparatorSelect = ADC12_B_WINDOW_COMPARATOR_DISABLE;
    XMemoryParam.differentialModeSelect = ADC12_B_DIFFERENTIAL_MODE_DISABLE;
    ADC12_B_configureMemory(ADC12_B_BASE, &XMemoryParam);

    ADC12_B_configureMemoryParam YMemoryParam = {0};
    YMemoryParam.memoryBufferControlIndex = ADC12_B_MEMORY_1;
    YMemoryParam.inputSourceSelect = ADC12_B_INPUT_A4;
    YMemoryParam.refVoltageSourceSelect = ADC12_B_VREFPOS_AVCC_VREFNEG_VSS;
    YMemoryParam.endOfSequence = ADC12_B_ENDOFSEQUENCE;
    YMemoryParam.windowComparatorSelect = ADC12_B_WINDOW_COMPARATOR_DISABLE;
    XMemoryParam.differentialModeSelect = ADC12_B_DIFFERENTIAL_MODE_DISABLE;
    ADC12_B_configureMemory(ADC12_B_BASE, &YMemoryParam);

    // ----------------------- ADC initialization end -----------------------

    // ----------------------- Buttons initialization start -----------------------
    // S1
    GPIO_setAsInputPin(GPIO_PORT_P3, GPIO_PIN0);
    // S2
    GPIO_setAsInputPin(GPIO_PORT_P3, GPIO_PIN1);
    // Joystick button
    GPIO_setAsInputPin(GPIO_PORT_P3, GPIO_PIN2);
    // ----------------------- Buttons initialization end -----------------------

    // ----------------------- LED initialization start -----------------------
    init_lcd();
    // ----------------------- LED initialization end -----------------------

    // ----------------------- UART initialization start -----------------------

    UARTStdioInit();
//    EUSCI_A_UART_enableInterrupt(EUSCI_A1_BASE, EUSCI_A_UART_STARTBIT_INTERRUPT);
//    EUSCI_A_UART_clearInterrupt(EUSCI_A1_BASE, EUSCI_A_UART_STARTBIT_INTERRUPT_FLAG);
//    __enable_interrupt();
}

void display_UI(){
    Graphics_clearDisplay(&g_sContext);
    Graphics_drawStringCentered(&g_sContext, (int8_t *)"SCORE:", AUTO_STRING_LENGTH, 64, 50, OPAQUE_TEXT);
}


void display_score(){
    Graphics_setForegroundColor(&g_sContext, GRAPHICS_COLOR_BLACK);
    Graphics_fillRectangle(&g_sContext, &score_text_box);
    Graphics_setForegroundColor(&g_sContext, GRAPHICS_COLOR_WHITE);
    Graphics_drawStringCentered(&g_sContext, (int8_t *)score, AUTO_STRING_LENGTH, 64, 60, OPAQUE_TEXT);
}

int main(void) {

    init();
    display_UI();
    display_score();

    ADC12_B_startConversion(ADC12_B_BASE,
                            ADC12_B_MEMORY_0,
                            ADC12_B_REPEATED_SEQOFCHANNELS);

    while(1)
    {

        long joystickX = ADC12_B_getResults(ADC12_B_BASE, ADC12_B_MEMORY_0);
        long joystickY = ADC12_B_getResults(ADC12_B_BASE, ADC12_B_MEMORY_1);
        long button1 = GPIO_getInputPinValue(GPIO_PORT_P3, GPIO_PIN0);
        long button2 = GPIO_getInputPinValue(GPIO_PORT_P3, GPIO_PIN1);
        long buttonj = GPIO_getInputPinValue(GPIO_PORT_P3, GPIO_PIN2);

    	UARTprintf("x:\%d y:\%d but1:\%d but2:\%d butj:\%d \n\r", joystickX, joystickY, button1, button2, buttonj);
        if(score_changed) {
            display_score();
            score_changed = 0;
        }

        __delay_cycles(1000);
    }
}


#pragma vector = USCI_A1_VECTOR
__interrupt void USCI_A1_ISR(void)
{
    uint16_t rx_status;
    rx_status = EUSCI_A_UART_getInterruptStatus(EUSCI_A1_BASE, EUSCI_A_UART_STARTBIT_INTERRUPT_FLAG);
    if(rx_status){
        UARTgets(score, 20);
    }
    score_changed = 1;
    __delay_cycles(20000);
    EUSCI_A_UART_clearInterrupt(EUSCI_A1_BASE, EUSCI_A_UART_STARTBIT_INTERRUPT_FLAG);
}
