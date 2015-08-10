/* -*- c++ -*- */
/* 
 * Copyright 2015 Red Balloon Security, Inc.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include "funtenna_demod_impl.h"

namespace gr {
  namespace funtenna_ook_demod {

    funtenna_demod::sptr
    funtenna_demod::make(int samp_thresh)
    {
      return gnuradio::get_initial_sptr
        (new funtenna_demod_impl(samp_thresh));
    }

    /*
     * The private constructor
     */
    funtenna_demod_impl::funtenna_demod_impl(int samp_thresh)
      : gr::block("funtenna_demod",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(unsigned char)))
    {
        set_thresh(samp_thresh);

        bitval = 0;
        sample_count = 0;
    }

    /*
     * Our virtual destructor.
     */
    funtenna_demod_impl::~funtenna_demod_impl()
    {
    }

    void
    funtenna_demod_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        ninput_items_required[0] = noutput_items;
    }

    void
    funtenna_demod_impl::set_thresh (int samp_thresh)
    {
        d_samp_thresh = samp_thresh;
    }

    int
    funtenna_demod_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const float *in = (const float *) input_items[0];
        unsigned char *out = (unsigned char *) output_items[0];
        int n = 0; 
       
        for (int i = 0; i < noutput_items; i++) {
            unsigned char this_bitval = (in[i] > 0.1) ? 1: 0;
            if (this_bitval != bitval) {
                // edge detect
                if (this_bitval == 1){
                    // rising edge, wait to count sample_length
                } else {
                    // falling edge, end of symbol...what was it???
                    if (sample_count < d_samp_thresh) {
                        // symbol was a zero
                        out[n++] = 0;
                    } else {
                        // symbol was a one
                        out[n++] = 1;
                    }
                    n = 1; 
                }
                sample_count = 0;
                bitval = this_bitval;
            }
            sample_count++;
        }
        // Tell runtime system how many input items we consumed on
        // each input stream.
        consume_each (noutput_items);
        // Tell runtime system how many output items we produced.
        return n;
    }

  } /* namespace funtenna_ook_demod */
} /* namespace gr */

