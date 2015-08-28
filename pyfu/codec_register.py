#!/usr/bin/env python
from __future__ import unicode_literals

#TODO: cStringIO
import io
import codecs, StringIO, encodings
from encodings import utf_8
import itertools

def decode(input, errors='strict'):
    return utf_8.decode(b'import pyfu ; pyfu.magic(__file__, __name__); del pyfu\n' + input, errors)


class IncrementalDecoder(utf_8.IncrementalDecoder):
    def __init__(self, errors='strict'):
        IncrementalDecoder.__init__(self, errors)
        self.buffer = b'import pyfu ; pyfu.magic(__file__, __name__); del pyfu\n' # undecoded input that is kept between calls to decode()


class StreamReader(utf_8.StreamReader):
    def __init__(self, *args, **kwargs):
        codecs.StreamReader.__init__(self, *args, **kwargs)
        self.stream = StringIO.StringIO(b'import pyfu ; pyfu.magic(__file__, __name__); del pyfu\n' + self.stream.read())


utf8_codec_info = encodings.search_function('utf8')
codec_info = codecs.CodecInfo(
    name='pyfu',
    encode=utf8_codec_info.encode,
    decode=decode,
    incrementalencoder=utf8_codec_info.incrementalencoder,
    incrementaldecoder=IncrementalDecoder,
    streamwriter=utf8_codec_info.streamwriter,
    streamreader=StreamReader,
)


def search_function(encoding):
    return codec_info if encoding == 'pyfu' else None

codecs.register(search_function)