################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Each subdirectory must supply rules for building sources it contributes
driverlib/MSP430FR5xx_6xx/%.obj: ../driverlib/MSP430FR5xx_6xx/%.c $(GEN_OPTS) | $(GEN_FILES) $(GEN_MISC_FILES)
	@echo 'Building file: "$<"'
	@echo 'Invoking: MSP430 Compiler'
	"/home/lab1361-10/programs/ti/ccs1200/ccs/tools/compiler/ti-cgt-msp430_21.6.0.LTS/bin/cl430" -vmspx --data_model=restricted -Ooff --use_hw_mpy=F5 --include_path="/home/lab1361-10/programs/ti/ccs1200/ccs/ccs_base/msp430/include" --include_path="/home/lab1361-10/Desktop/iantov/MSP430_controller/GrLib/grlib" --include_path="/home/lab1361-10/Desktop/iantov/MSP430_controller/LcdDriver" --include_path="/home/lab1361-10/Desktop/iantov/MSP430_controller/driverlib/MSP430FR5xx_6xx" --include_path="/home/lab1361-10/programs/ti/ccs1200/ccs/tools/compiler/ti-cgt-msp430_21.6.0.LTS/include" --advice:power="all" --advice:hw_config="all" -g --define=__MSP430FR6989__ --define=ccs --define=_MPU_ENABLE --display_error_number --diag_wrap=off --diag_warning=225 --silicon_errata=CPU21 --silicon_errata=CPU22 --silicon_errata=CPU40 --printf_support=full --preproc_with_compile --preproc_dependency="driverlib/MSP430FR5xx_6xx/$(basename $(<F)).d_raw" --obj_directory="driverlib/MSP430FR5xx_6xx" $(GEN_OPTS__FLAG) "$(shell echo $<)"
	@echo 'Finished building: "$<"'
	@echo ' '


