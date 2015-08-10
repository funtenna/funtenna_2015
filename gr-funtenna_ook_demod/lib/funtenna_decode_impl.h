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

#ifndef INCLUDED_FUNTENNA_OOK_DEMOD_FUNTENNA_DECODE_IMPL_H
#define INCLUDED_FUNTENNA_OOK_DEMOD_FUNTENNA_DECODE_IMPL_H

#include <funtenna_ook_demod/funtenna_decode.h>

namespace gr {
  namespace funtenna_ook_demod {

    class funtenna_decode_impl : public funtenna_decode
    {
     private:
        std::vector<int> d_preamble;
        bool sync;
        std::vector<int>::size_type sync_idx;
        
        int bit_count;
        int sym_idx;
        unsigned char cur_sym;

     public:
      funtenna_decode_impl(const std::vector<int> &preamble);
      ~funtenna_decode_impl();

      void forecast (int noutput_items, gr_vector_int &ninput_items_required);
      
      // Where all the action really happens
      int general_work(int noutput_items,
		       gr_vector_int &ninput_items,
		       gr_vector_const_void_star &input_items,
		       gr_vector_void_star &output_items);
      
      void preamble_sync(unsigned char bit);
      bool decode_byte(unsigned char bit);

    };

  } // namespace funtenna_ook_demod
} // namespace gr

#endif /* INCLUDED_FUNTENNA_OOK_DEMOD_FUNTENNA_DECODE_IMPL_H */

