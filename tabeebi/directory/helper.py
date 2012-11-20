import gc
import unicodedata

def queryset_iterator(queryset, batchsize = 500, gc_collect = True):
    """
    Very useful for large queries where splitting up under the old system would result in
    a very slow query (as a large amount of results are likely sorted and mostly discarded).
    The secret is maintaining the fully sorted list (with only pk to minimize temporary table size)
    with a database cursor, and processing it in batches to get the full results.
    """
    iterator = queryset.values_list('pk', flat = True).distinct().iterator()
    eof = False
    while not eof:
        primary_key_buffer = []
        try:
            while len(primary_key_buffer) < batchsize:
                primary_key_buffer.append(iterator.next())
        except StopIteration:
            eof = True

        for result in queryset.filter(pk__in = primary_key_buffer).iterator():
            yield result

        if gc_collect:
            gc.collect()


def unicode_to_string(unicode_string, format = 'ascii'):
    return unicodedata.normalize('NFKD', unicode_string).encode(format, 'ignore')