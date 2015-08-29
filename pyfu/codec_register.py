#!/usr/bin/env python

#TODO: cStringIO
import codecs, StringIO, encodings
from encodings import utf_8


def decode(input, errors='strict'):
    return utf_8.decode(b'import pyfu ; pyfu.magic(__file__, __name__); del pyfu', errors)


class IncrementalDecoder(utf_8.IncrementalDecoder):

    def decode(self, input, final=False):
        if final:
            return super(IncrementalDecoder, self).decode(b'import pyfu ; pyfu.magic(__file__, __name__); del pyfu', final=True)


class StreamReader(utf_8.StreamReader):

    def __init__(self, *args, **kwargs):
        codecs.StreamReader.__init__(self, *args, **kwargs)
        self.stream = StringIO.StringIO(b'import pyfu ; pyfu.magic(__file__, __name__); del pyfu')


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
    if encoding == 'pyfu':
        return codec_info

codecs.register(search_function)