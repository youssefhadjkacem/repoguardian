from datetime import date

import pytest

from taskapi import TaskStore


def test_add_and_get():
    store = TaskStore()
    task = store.add("Écrire le README", priority="high")
    assert store.get(task.id).title == "Écrire le README"


def test_add_rejects_empty_title():
    with pytest.raises(ValueError):
        TaskStore().add("   ")


def test_add_rejects_unknown_priority():
    with pytest.raises(ValueError):
        TaskStore().add("x", priority="urgent")


def test_complete_removes_from_pending():
    store = TaskStore()
    t = store.add("A")
    store.add("B")
    store.complete(t.id)
    assert [x.title for x in store.pending()] == ["B"]


def test_overdue_detects_past_due():
    store = TaskStore()
    store.add("Vieux", due=date(2026, 1, 1))
    assert len(store.overdue(today=date(2026, 6, 1))) == 1