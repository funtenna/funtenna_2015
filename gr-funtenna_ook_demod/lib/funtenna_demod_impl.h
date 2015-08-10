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

#ifndef INCLUDED_FUNTENNA_OOK_DEMOD_FUNTENNA_DEMOD_IMPL_H
#define INCLUDED_FUNTENNA_OOK_DEMOD_FUNTENNA_DEMOD_IMPL_H

#include <funtenna_ook_demod/funtenna_demod.h>

namespace gr {
  namespace funtenna_ook_demod {

    class funtenna_demod_impl : public funtenna_demod
    {
     private:
        unsigned int bitval;
        int sample_count;
        //demod_state_t state;
        int d_samp_thresh;
      // Nothing to declare in this block.

     public:
      funtenna_demod_impl(int samp_thresh);
      ~funtenna_demod_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
		       gr_vector_int &ninput_items,
		       gr_vector_const_void_star &input_items,
		       gr_vector_void_star &output_items);

      int samp_thresh() const { return d_samp_thresh;}
      void set_thresh(int samp_thresh);
    };

  } // namespace funtenna_ook_demod
} // namespace gr

#endif /* INCLUDED_FUNTENNA_OOK_DEMOD_funtenna_DEMOD_IMPL_H */

