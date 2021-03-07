from timeline.timeline import Timeline
from timeline.event import Event

def test_timeline_iterate():
    """
    Create a timeline with 3 events and check that we can iterate over them correcly
    """
    event1 = Event("1", "1978", "__")
    event2 = Event("2", "1 Sep 1997", "31 Jul 2000")
    event3 = Event("3", "01/12/1990", "31/08/1997")
    timeline = Timeline([event1, event2, event3])
    output = []
    for event in timeline:
        output.append(event)
    assert output[0] == event1
    assert output[1] == event3
    assert output[2] == event2
