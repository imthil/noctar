#!/bin/sh

UTIL=langford_util
UTIL_ADC=langford_adc_util
FSYNTH=langford_rf_fsynth
VGA=langford_rx_rf_bb_vga
DEVICE=/dev/langford

#Enable HF chain
$UTIL $DEVICE NASRxA 0

#Set HF gain to 1
$UTIL $DEVICE N21at0 1

#Set frequency synthesizer
$FSYNTH $DEVICE rx 400e6

#Set ADC VGA to reasonable values on both channels
$VGA $DEVICE 0 15.5
$VGA $DEVICE 1 15.5

#Enable decimation of 2
$UTIL $DEVICE RXDecEn 0x1

#Set RXRevFreq to 0
$UTIL $DEVICE RXRevFreq 0

#Set RXPhase
$UTIL $DEVICE RXPhase 15461882265

#Ensure Simultanious ADC Clocking (no interleaving)
$UTIL_ADC $DEVICE A ClkSel 0
$UTIL_ADC $DEVICE B ClkSel 0

$UTIL $DEVICE NASTxA 1

$UTIL $DEVICE TXIntEn 0x0

$UTIL $DEVICE NRXTALSEL 1

$UTIL $DEVICE NRVCOSEL 1

$UTIL $DEVICE DACSDO 0

gnuradio-companion nbfm_rx.grc
