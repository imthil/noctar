#!/usr/bin/env python2
##################################################
# Gnuradio Python Flow Graph
# Title: NBFM Receiver
# Author: Thilina Mallawa Arachchi
# Description: A simple narrow-band FM receiver using the noctar SDR
# Generated: Thu Jun 26 08:41:33 2014
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import wx

class nbfm_rx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="NBFM Receiver")

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 125e6

        ##################################################
        # Blocks
        ##################################################
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=450e6,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Waterfall Plot",
        )
        self.Add(self.wxgui_waterfallsink2_0.win)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=3,
                decimation=125,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=48,
                decimation=30,
                taps=None,
                fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(10, firdes.low_pass(
        	1, 3e6, 5e3, 2e3, firdes.WIN_HAMMING, 6.76))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((10, ))
        self.blocks_interleaved_short_to_complex_0 = blocks.interleaved_short_to_complex(False, False)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_short*1, "/dev/langford", True)
        self.audio_sink_0 = audio.sink(48000, "", True)
        self.analog_pwr_squelch_xx_1 = analog.pwr_squelch_cc(-80, 1, 0, False)
        self.analog_nbfm_rx_0 = analog.nbfm_rx(
        	audio_rate=30000,
        	quad_rate=300000,
        	tau=75e-6,
        	max_dev=5e3,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_interleaved_short_to_complex_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_nbfm_rx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_nbfm_rx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.wxgui_waterfallsink2_0, 0))
        self.connect((self.blocks_interleaved_short_to_complex_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_pwr_squelch_xx_1, 0))
        self.connect((self.analog_pwr_squelch_xx_1, 0), (self.low_pass_filter_0, 0))



    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = nbfm_rx()
    tb.Start(True)
    tb.Wait()
