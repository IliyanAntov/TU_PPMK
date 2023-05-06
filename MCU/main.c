#include <stdio.h>
#include <driverlib.h>
#include <math.h>
#include "grlib.h"
#include "Crystalfontz128x128_ST7735.h"
#include "uartstdio.h"

#define MAX_STR_SIZE	20

volatile char score[20] = {"#####"};
volatile int score_changed = 0;

/* Graphic library context */
Graphics_Context g_sContext;
Graphics_Rectangle score_text_box;


void init_clock_system(void) {
    CS_setDCOFreq(CS_DCORSEL_1, CS_DCOFSEL_4); //DCO = 16 MHz
    CS_initClockSignal(CS_SMCLK, CS_DCOCLK_SELECT, CS_CLOCK_DIVIDER_1); //SMCLK = DCO clock
}

void init_ADC(void) {
    // Setup the analog pin connected to the X axis of the joystick
    GPIO_setAsInputPin(GPIO_PORT_P9, GPIO_PIN2);
    GPIO_setAsPeripheralModuleFunctionInputPin(GPIO_PORT_P9, GPIO_PIN2, GPIO_TERNARY_MODULE_FUNCTION);
    // Setup the analog pin connected to the Y axis of the joystick
    GPIO_setAsInputPin(GPIO_PORT_P8, GPIO_PIN7);
    GPIO_setAsPeripheralModuleFunctionInputPin(GPIO_PORT_P8, GPIO_PIN7, GPIO_TERNARY_MODULE_FUNCTION);

    // Initialize the ADC
    ADC12_B_initParam adc_init_struct;
    adc_init_struct.sampleHoldSignalSourceSelect = ADC12_B_SAMPLEHOLDSOURCE_SC;
    adc_init_struct.clockSourceSelect = ADC12_B_CLOCKSOURCE_SMCLK;
    adc_init_struct.clockSourceDivider = ADC12_B_CLOCKDIVIDER_1;
    adc_init_struct.clockSourcePredivider = ADC12_B_CLOCKPREDIVIDER__1;
    adc_init_struct.internalChannelMap = ADC12_B_MAPINTCH0;
    ADC12_B_init(ADC12_B_BASE, &adc_init_struct);
    
    // Enable the ADC
    ADC12_B_enable(ADC12_B_BASE);

    // Setup the sample and hold module
    ADC12_B_setupSamplingTimer(ADC12_B_BASE,
                               ADC12_B_CYCLEHOLD_16_CYCLES,
                               ADC12_B_CYCLEHOLD_4_CYCLES,
                               ADC12_B_MULTIPLESAMPLESENABLE);


    // Setup the memory registers that will store X axis values
    ADC12_B_configureMemoryParam XMemoryParam = {0};
    XMemoryParam.memoryBufferControlIndex = ADC12_B_MEMORY_0;
    XMemoryParam.inputSourceSelect = ADC12_B_INPUT_A10;
    XMemoryParam.refVoltageSourceSelect = ADC12_B_VREFPOS_AVCC_VREFNEG_VSS;
    XMemoryParam.endOfSequence = ADC12_B_NOTENDOFSEQUENCE;
    XMemoryParam.windowComparatorSelect = ADC12_B_WINDOW_COMPARATOR_DISABLE;
    XMemoryParam.differentialModeSelect = ADC12_B_DIFFERENTIAL_MODE_DISABLE;
    ADC12_B_configureMemory(ADC12_B_BASE, &XMemoryParam);

    // Setup the memory registers that will store Y axis values
    ADC12_B_configureMemoryParam YMemoryParam = {0};
    YMemoryParam.memoryBufferControlIndex = ADC12_B_MEMORY_1;
    YMemoryParam.inputSourceSelect = ADC12_B_INPUT_A4;
    YMemoryParam.refVoltageSourceSelect = ADC12_B_VREFPOS_AVCC_VREFNEG_VSS;
    YMemoryParam.endOfSequence = ADC12_B_ENDOFSEQUENCE;
    YMemoryParam.windowComparatorSelect = ADC12_B_WINDOW_COMPARATOR_DISABLE;
    XMemoryParam.differentialModeSelect = ADC12_B_DIFFERENTIAL_MODE_DISABLE;
    ADC12_B_configureMemory(ADC12_B_BASE, &YMemoryParam);
}

void init_buttons(void) {
    // S1
    GPIO_setAsInputPin(GPIO_PORT_P3, GPIO_PIN0);
    // S2
    GPIO_setAsInputPin(GPIO_PORT_P3, GPIO_PIN1);
    // Joystick button
    GPIO_setAsInputPin(GPIO_PORT_P3, GPIO_PIN2);
}

void init_LCD(void) {
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

void init_UART(void) {
    // Initialize the UART module
    UARTStdioInit();
    // Enable and clear RX interrupts
    EUSCI_A_UART_enableInterrupt(EUSCI_A1_BASE, EUSCI_A_UART_STARTBIT_INTERRUPT);
    EUSCI_A_UART_clearInterrupt(EUSCI_A1_BASE, EUSCI_A_UART_STARTBIT_INTERRUPT_FLAG);
}

void init(void) {
    // Stop the watchdog timer
    WDT_A_hold(WDT_A_BASE);
    // Disable the GPIO power-on default high-impedance mode to activate previously configured port settings
    PMM_unlockLPM5();

    FRAMCtl_configureWaitStateControl(FRAMCTL_ACCESS_TIME_CYCLES_1); //Needed for DCO = 16 MHz

    // Initialize the clock system
    init_clock_system();

    // Initialize the ADC used for reading joystick values
    init_ADC();

    // Initialize all buttons
    init_buttons();

    // Initialize the LCD screen
    init_LCD();

    // Initialize the UART module user for sending and receiving information from the computer app
    init_UART();

    // Enable interrupts globally
    __enable_interrupt();
}


void display_UI(void) {
    // Clear the display
    Graphics_clearDisplay(&g_sContext);
    // Display the basic UI
    Graphics_drawStringCentered(&g_sContext, (int8_t *)"SCORE:", AUTO_STRING_LENGTH, 64, 50, OPAQUE_TEXT);
}

void display_score(void) {
    // Draw a black box over the old score
    Graphics_setForegroundColor(&g_sContext, GRAPHICS_COLOR_BLACK);
    Graphics_fillRectangle(&g_sContext, &score_text_box);
    // Display the current score
    Graphics_setForegroundColor(&g_sContext, GRAPHICS_COLOR_WHITE);
    Graphics_drawStringCentered(&g_sContext, (int8_t *)score, AUTO_STRING_LENGTH, 64, 60, OPAQUE_TEXT);
}


int main(void) {
    // Initialize all modules 
    init();
    // Display the LCD UI
    display_UI();
    // Display the initial score
    display_score();
    
    // Start reading joystick X and Y values repeatedly
    ADC12_B_startConversion(ADC12_B_BASE,
                            ADC12_B_MEMORY_0,
                            ADC12_B_REPEATED_SEQOFCHANNELS);

    while(1) {

        // Extract the current controller state
        long joystickX = ADC12_B_getResults(ADC12_B_BASE, ADC12_B_MEMORY_0);
        long joystickY = ADC12_B_getResults(ADC12_B_BASE, ADC12_B_MEMORY_1);
        long button1 = GPIO_getInputPinValue(GPIO_PORT_P3, GPIO_PIN0);
        long button2 = GPIO_getInputPinValue(GPIO_PORT_P3, GPIO_PIN1);
        long buttonj = GPIO_getInputPinValue(GPIO_PORT_P3, GPIO_PIN2);

        // Create a standard string with the current controller state and send it via the UART interface
    	UARTprintf("x:\%d y:\%d but1:\%d but2:\%d butj:\%d \n\r", joystickX, joystickY, button1, button2, buttonj);
        
        // If the score has changed since the last iteration, display the new value and reset the flag
        if(score_changed) {
            display_score();
            score_changed = 0;
        }

        __delay_cycles(1000);
    }
}


#pragma vector = USCI_A1_VECTOR
__interrupt void USCI_A1_ISR(void) {
    // Get the UART RX interrupt status
    uint16_t rx_status;
    rx_status = EUSCI_A_UART_getInterruptStatus(EUSCI_A1_BASE, EUSCI_A_UART_STARTBIT_INTERRUPT_FLAG);
    
    // If there is incoming data, read and save it to the score variable
    if(rx_status) {
        UARTgets(score, 20);
    }

    // Raise the score change flag
    score_changed = 1;
    __delay_cycles(20000);

    // Clear the UART RX interrupt
    EUSCI_A_UART_clearInterrupt(EUSCI_A1_BASE, EUSCI_A_UART_STARTBIT_INTERRUPT_FLAG);
}
