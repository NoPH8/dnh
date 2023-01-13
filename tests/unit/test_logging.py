from app.logging import FIFOTemporaryStream


def test_fifo_temporary_stream():
    stream = FIFOTemporaryStream()
    stream.write('Test msg')

    assert list(stream.show()) == ['Test msg']
