#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Funtenna Demod
# Generated: Mon Aug 10 12:47:11 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import funtenna_ook_demod
import wx

class funtenna_demod(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Funtenna Demod")

        ##################################################
        # Variables
        ##################################################
        self.symbol_threshold = symbol_threshold = .4
        self.sample_threshold = sample_threshold = 115
        self.samp_rate = samp_rate = 250000
        self.initial_dec = initial_dec = 20
        self.complex_dec = complex_dec = 10
        self.center_freq = center_freq = 29494830
        self.bandwidth = bandwidth = 550
        self.amplitude_filter = amplitude_filter = 10
        self.amplitude_dec = amplitude_dec = 1

        ##################################################
        # Blocks
        ##################################################
        self._symbol_threshold_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.symbol_threshold,
        	callback=self.set_symbol_threshold,
        	label="Amplitude Threshold (n)",
        	converter=forms.float_converter(),
        )
        self.Add(self._symbol_threshold_text_box)
        self._sample_threshold_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.sample_threshold,
        	callback=self.set_sample_threshold,
        	label="Sample Threshold",
        	converter=forms.float_converter(),
        )
        self.Add(self._sample_threshold_text_box)
        self.notebook_0 = self.notebook_0 = wx.Notebook(self.GetWin(), style=wx.NB_TOP)
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "tab1")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "tab2")
        self.notebook_0.AddPage(grc_wxgui.Panel(self.notebook_0), "tab3")
        self.Add(self.notebook_0)
        self._initial_dec_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.initial_dec,
        	callback=self.set_initial_dec,
        	label="Initial Decimation",
        	converter=forms.float_converter(),
        )
        self.Add(self._initial_dec_text_box)
        _complex_dec_sizer = wx.BoxSizer(wx.VERTICAL)
        self._complex_dec_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_complex_dec_sizer,
        	value=self.complex_dec,
        	callback=self.set_complex_dec,
        	label="Complex Filter Decimation",
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._complex_dec_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_complex_dec_sizer,
        	value=self.complex_dec,
        	callback=self.set_complex_dec,
        	minimum=1,
        	maximum=400,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.Add(_complex_dec_sizer)
        self._center_freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.center_freq,
        	callback=self.set_center_freq,
        	label="Center Frequency",
        	converter=forms.float_converter(),
        )
        self.Add(self._center_freq_text_box)
        self._bandwidth_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.bandwidth,
        	callback=self.set_bandwidth,
        	label="Bandwidth",
        	converter=forms.float_converter(),
        )
        self.Add(self._bandwidth_text_box)
        self._amplitude_filter_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.amplitude_filter,
        	callback=self.set_amplitude_filter,
        	label="Amplitude Filter (Hz)",
        	converter=forms.float_converter(),
        )
        self.Add(self._amplitude_filter_text_box)
        _amplitude_dec_sizer = wx.BoxSizer(wx.VERTICAL)
        self._amplitude_dec_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_amplitude_dec_sizer,
        	value=self.amplitude_dec,
        	callback=self.set_amplitude_dec,
        	label="Amplitude Decimation",
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._amplitude_dec_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_amplitude_dec_sizer,
        	value=self.amplitude_dec,
        	callback=self.set_amplitude_dec,
        	minimum=0,
        	maximum=1000,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.Add(_amplitude_dec_sizer)
        self.wxgui_waterfallsink2_0_0 = waterfallsink2.waterfall_sink_c(
        	self.notebook_0.GetPage(0).GetWin(),
        	baseband_freq=0,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate/initial_dec,
        	fft_size=256,
        	fft_rate=65,
        	average=False,
        	avg_alpha=None,
        	title="Decimated IQ",
        )
        self.notebook_0.GetPage(0).Add(self.wxgui_waterfallsink2_0_0.win)
        self.wxgui_scopesink2_1 = scopesink2.scope_sink_f(
        	self.notebook_0.GetPage(0).GetWin(),
        	title="Filtered Magnitude",
        	sample_rate=samp_rate/initial_dec/complex_dec/amplitude_dec,
        	v_scale=.000000005,
        	v_offset=0,
        	t_scale=.5,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.notebook_0.GetPage(0).Add(self.wxgui_scopesink2_1.win)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.notebook_0.GetPage(1).GetWin(),
        	title="Pre-demod",
        	sample_rate=samp_rate/initial_dec/complex_dec/amplitude_dec,
        	v_scale=1,
        	v_offset=.00000,
        	t_scale=0.5,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label="Counts",
        )
        self.notebook_0.GetPage(1).Add(self.wxgui_scopesink2_0.win)
        self.low_pass_filter_0_0 = filter.fir_filter_fff(amplitude_dec, firdes.low_pass(
        	1, (samp_rate/initial_dec)/complex_dec, amplitude_filter, 50, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(complex_dec, firdes.low_pass(
        	1, samp_rate/initial_dec, bandwidth, 20, firdes.WIN_HAMMING, 6.76))
        self.funtenna_ook_demod_funtenna_demod_1 = funtenna_ook_demod.funtenna_demod(sample_threshold)
        self.funtenna_ook_demod_funtenna_decode_1 = funtenna_ook_demod.funtenna_decode(([1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(initial_dec, (1, ), center_freq, samp_rate)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(.000000001 * symbol_threshold, .000000001 * symbol_threshold, 0)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, "./funtenna_iq.bin", True)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_char*1, "./funtenna_out.txt", False)
        self.blocks_file_sink_0.set_unbuffered(True)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.low_pass_filter_0_0, 0))    
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.funtenna_ook_demod_funtenna_demod_1, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.wxgui_waterfallsink2_0_0, 0))    
        self.connect((self.funtenna_ook_demod_funtenna_decode_1, 0), (self.blocks_file_sink_0, 0))    
        self.connect((self.funtenna_ook_demod_funtenna_demod_1, 0), (self.funtenna_ook_demod_funtenna_decode_1, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.low_pass_filter_0_0, 0), (self.wxgui_scopesink2_1, 0))    


    def get_symbol_threshold(self):
        return self.symbol_threshold

    def set_symbol_threshold(self, symbol_threshold):
        self.symbol_threshold = symbol_threshold
        self._symbol_threshold_text_box.set_value(self.symbol_threshold)
        self.blocks_threshold_ff_0.set_hi(.000000001 * self.symbol_threshold)
        self.blocks_threshold_ff_0.set_lo(.000000001 * self.symbol_threshold)

    def get_sample_threshold(self):
        return self.sample_threshold

    def set_sample_threshold(self, sample_threshold):
        self.sample_threshold = sample_threshold
        self._sample_threshold_text_box.set_value(self.sample_threshold)
        self.funtenna_ook_demod_funtenna_demod_1.set_thresh(self.sample_threshold)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate/self.initial_dec, self.bandwidth, 20, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, (self.samp_rate/self.initial_dec)/self.complex_dec, self.amplitude_filter, 50, firdes.WIN_HAMMING, 6.76))
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate/self.initial_dec/self.complex_dec/self.amplitude_dec)
        self.wxgui_scopesink2_1.set_sample_rate(self.samp_rate/self.initial_dec/self.complex_dec/self.amplitude_dec)
        self.wxgui_waterfallsink2_0_0.set_sample_rate(self.samp_rate/self.initial_dec)

    def get_initial_dec(self):
        return self.initial_dec

    def set_initial_dec(self, initial_dec):
        self.initial_dec = initial_dec
        self._initial_dec_text_box.set_value(self.initial_dec)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate/self.initial_dec, self.bandwidth, 20, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, (self.samp_rate/self.initial_dec)/self.complex_dec, self.amplitude_filter, 50, firdes.WIN_HAMMING, 6.76))
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate/self.initial_dec/self.complex_dec/self.amplitude_dec)
        self.wxgui_scopesink2_1.set_sample_rate(self.samp_rate/self.initial_dec/self.complex_dec/self.amplitude_dec)
        self.wxgui_waterfallsink2_0_0.set_sample_rate(self.samp_rate/self.initial_dec)

    def get_complex_dec(self):
        return self.complex_dec

    def set_complex_dec(self, complex_dec):
        self.complex_dec = complex_dec
        self._complex_dec_slider.set_value(self.complex_dec)
        self._complex_dec_text_box.set_value(self.complex_dec)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, (self.samp_rate/self.initial_dec)/self.complex_dec, self.amplitude_filter, 50, firdes.WIN_HAMMING, 6.76))
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate/self.initial_dec/self.complex_dec/self.amplitude_dec)
        self.wxgui_scopesink2_1.set_sample_rate(self.samp_rate/self.initial_dec/self.complex_dec/self.amplitude_dec)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self._center_freq_text_box.set_value(self.center_freq)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(self.center_freq)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self._bandwidth_text_box.set_value(self.bandwidth)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate/self.initial_dec, self.bandwidth, 20, firdes.WIN_HAMMING, 6.76))

    def get_amplitude_filter(self):
        return self.amplitude_filter

    def set_amplitude_filter(self, amplitude_filter):
        self.amplitude_filter = amplitude_filter
        self._amplitude_filter_text_box.set_value(self.amplitude_filter)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, (self.samp_rate/self.initial_dec)/self.complex_dec, self.amplitude_filter, 50, firdes.WIN_HAMMING, 6.76))

    def get_amplitude_dec(self):
        return self.amplitude_dec

    def set_amplitude_dec(self, amplitude_dec):
        self.amplitude_dec = amplitude_dec
        self._amplitude_dec_slider.set_value(self.amplitude_dec)
        self._amplitude_dec_text_box.set_value(self.amplitude_dec)
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate/self.initial_dec/self.complex_dec/self.amplitude_dec)
        self.wxgui_scopesink2_1.set_sample_rate(self.samp_rate/self.initial_dec/self.complex_dec/self.amplitude_dec)


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = funtenna_demod()
    tb.Start(True)
    tb.Wait()
