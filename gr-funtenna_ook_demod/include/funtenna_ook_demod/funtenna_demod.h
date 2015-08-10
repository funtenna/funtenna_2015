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


#ifndef INCLUDED_FUNTENNA_OOK_DEMOD_FUNTENNA_DEMOD_H
#define INCLUDED_FUNTENNA_OOK_DEMOD_FUNTENNA_DEMOD_H

#include <funtenna_ook_demod/api.h>
#include <gnuradio/block.h>

namespace gr {
  namespace funtenna_ook_demod {

    /*!
     * \brief <+description of block+>
     * \ingroup funtenna_ook_demod
     *
     */
    class FUNTENNA_OOK_DEMOD_API funtenna_demod : virtual public gr::block
    {
     public:
      typedef boost::shared_ptr<funtenna_demod> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of funtenna_ook_demod::funtenna_demod.
       *
       * To avoid accidental use of raw pointers, funtenna_ook_demod::funtenna_demod's
       * constructor is in a private implementation
       * class. funtenna_ook_demod::funtenna_demod::make is the public interface for
       * creating new instances.
       */
      static sptr make(int samp_thresh);

      virtual int samp_thresh() const = 0;

      virtual void set_thresh(int samp_thresh) = 0;
    };

  } // namespace funtenna_ook_demod
} // namespace gr

#endif /* INCLUDED_FUNTENNA_OOK_DEMOD_FUNTENNA_DEMOD_H */

