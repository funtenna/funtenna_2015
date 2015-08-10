/* -*- c++ -*- */

#define FUNTENNA_OOK_DEMOD_API

%include "gnuradio.i"			// the common stuff

//load generated python docstrings
%include "funtenna_ook_demod_swig_doc.i"

%{
#include "funtenna_ook_demod/funtenna_demod.h"
#include "funtenna_ook_demod/funtenna_decode.h"
%}


%include "funtenna_ook_demod/funtenna_demod.h"
GR_SWIG_BLOCK_MAGIC2(funtenna_ook_demod, funtenna_demod);
%include "funtenna_ook_demod/funtenna_decode.h"
GR_SWIG_BLOCK_MAGIC2(funtenna_ook_demod, funtenna_decode);
