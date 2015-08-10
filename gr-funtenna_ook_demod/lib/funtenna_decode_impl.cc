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

#include <iostream>
#include <gnuradio/io_signature.h>
#include "funtenna_decode_impl.h"

namespace gr {
  namespace funtenna_ook_demod {

    funtenna_decode::sptr
    funtenna_decode::make(const std::vector<int> &preamble)
    {
      return gnuradio::get_initial_sptr
        (new funtenna_decode_impl(preamble));
    }

    /*
     * The private constructor
     */
    funtenna_decode_impl::funtenna_decode_impl(const std::vector<int> &preamble)
      : gr::block("funtenna_decode",
              gr::io_signature::make(1, 1, sizeof(unsigned char)),
              gr::io_signature::make(1, 1, sizeof(unsigned char)))
    {
        d_preamble = preamble;
        sync = false;
        sync_idx = 0;
        sym_idx = 0;
    }

    /*
     * Our virtual destructor.
     */
    funtenna_decode_impl::~funtenna_decode_impl()
    {
    }
    
    /*
     * Add me to header file
     */
    void
    funtenna_decode_impl::preamble_sync (unsigned char bit)
    {
        int bitval; 
        bitval = (int)bit;

        if (sync_idx < d_preamble.size()-1) {
            if (bitval == d_preamble[sync_idx]) {
                sync_idx++;
            } else if (bitval == d_preamble[0]) {
                sync_idx = 1;
            } else {
                sync_idx = 0;
            }
            std::cout << "\tsync_idx: " << sync_idx << "\r\n";
        } else {
            sync_idx = 0;
            sync = true;
            cur_sym = 0;
            std::cout << "\nSync!\n@";
        }

    }

    bool
    funtenna_decode_impl::decode_byte (unsigned char bit)
    {
        bool ret_val = false;
        cur_sym |= bit << (4-sym_idx++);
 
         if (sym_idx == 5) {  
            sym_idx = 0;
            ret_val = true;
            cur_sym +=64;
         }

        return ret_val;
    }
    
    void
    funtenna_decode_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
        ninput_items_required[0] = noutput_items;
    }

    int
    funtenna_decode_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
        const unsigned char *in = (const unsigned char *) input_items[0];
        unsigned char *out = (unsigned char *) output_items[0];
        int n;
        
        for (int i = 0; i < noutput_items; i++) {
            n = 0;
	        std::cout << std::flush;
            if (!sync) {
                // look for preamble default=0xaaaa
                preamble_sync(in[i]); 
            } else {
                if (in[i] == 1) {
                    std::cout << "1";
                } else if (in[i] == 0) {
                    std::cout << "0";
                }
	    
                //decode packet until 0xffff, discard 0's at end of word
                if (decode_byte(in[i]) == true) {
                    //symbol ready
                    if (cur_sym != 0x5f) {
                        out[0] = cur_sym;
                        n = 1;
		            	std::cout << "\n";
                        std::cout << "$" << cur_sym << "\n@";
                    } else {
                        std::cout << "\nUnsync!\n";
                        sync = false;
                    }
                    cur_sym = 0;
                }
            }
        }
        
        // Tell runtime system how many input items we consumed on
        // each input stream.
        consume_each (noutput_items);

        // Tell runtime system how many output items we produced.
        return n;
    }

  } /* namespace funtenna_ook_demod */
} /* namespace gr */

