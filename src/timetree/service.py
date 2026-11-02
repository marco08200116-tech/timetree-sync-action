from timetree_exporter.api.auth import login
from timetree_exporter.api.calendar import TimeTreeCalendar
from timetree_exporter.calendar import Calendar


class TimeTreeService:
    """Bridge to the bundled TimeTree-exporter."""

    def login(self, email: str, password: str) -> None:
        session_id = login(email, password)
        if session_id is None:
            raise RuntimeError("Failed to login to TimeTree.")
        self._calendar_api = TimeTreeCalendar(session_id)

    def get_calendars(self) -> list[dict]:
        if not hasattr(self, "_calendar_api"):
            raise RuntimeError("Not logged in.")
        calendars = self._calendar_api.get_metadata()
        return [
            calendar for calendar in calendars if calendar["deactivated_at"] is None
        ]

    def get_calendar(self, alias_code: str) -> Calendar:
        calendars = self.get_calendars()
        print("Available TimeTree calendars:")
        for c in calendars:
            print(f"- {c['name']} (code={c['alias_code']})")

        for metadata in calendars:
            if metadata["alias_code"] == alias_code:
                return Calendar(
                    api=self._calendar_api,
                    metadata=metadata,
                )
        raise RuntimeError(f"Calendar '{alias_code}' not found.")

    def get_events(self, calendar: Calendar):
        events = calendar.get_events()
        users = calendar.metadata.get("calendar_users") or []
        for u in users:
            print(
                "DEBUG user:",
                "id=", u.get("id"),
                "user_id=", u.get("user_id"),
                "primary_id=", u.get("primary_id"),
                "name=", u.get("name"),
            )
        for e in events:
            print(
                "DEBUG ev:",
                "author_id=", e.get("author_id"),
                "author_type=", e.get("author_type"),
                "label_id=", e.get("label_id"),
                "title=", e.get("title"),
            )
        return events
