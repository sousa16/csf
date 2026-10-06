#!/usr/bin/env python3
# evtx_dump.py -- read a Windows .evtx file with pyevtx (libevtx), read-only.
#
# usage:
#   evtx_dump.py count <file.evtx>            histogram of event IDs
#   evtx_dump.py show <file.evtx> [id ...]     print time + XML for each record,
#                                               optionally filtered to given IDs

import sys
import pyevtx


def records(path):
    f = pyevtx.file()
    f.open(path)
    for i in range(f.get_number_of_records()):
        yield f.get_record(i)


def event_id(rec):
    # pyevtx exposes event_identifier directly on newer builds; fall back to
    # pulling <EventID> out of the XML for older ones.
    try:
        return rec.get_event_identifier()
    except AttributeError:
        import re
        m = re.search(r"<EventID[^>]*>(\d+)</EventID>", rec.get_xml_string())
        return int(m.group(1)) if m else None


def main():
    cmd, path = sys.argv[1], sys.argv[2]
    if cmd == "count":
        from collections import Counter
        c = Counter(event_id(r) for r in records(path))
        for eid, n in c.most_common():
            print(f"{eid}\t{n}")
    elif cmd == "show":
        ids = {int(x) for x in sys.argv[3:]} if len(sys.argv) > 3 else None
        for r in records(path):
            eid = event_id(r)
            if ids and eid not in ids:
                continue
            print(f"--- record {r.get_offset()} event_id={eid} written={r.get_written_time()}")
            print(r.get_xml_string())
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
