
from nio import MatrixRoom, RoomMessageText


class Callbacks:
    def __init__(self, client, sugaroid):
        self.client = client
        self.sugaroid = sugaroid

    async def message(self, room: MatrixRoom, event: RoomMessageText) -> None:
        print(
            f"Message received in room {room.display_name}\n"
            f"{room.user_name(event.sender)} | {event.body}"
        )

        if event.body.startswith("!S"):
            msg = event.body.lstrip("!S").strip()
        elif event.body.startswith("sugaroid:"):
            msg = event.body.lstrip("sugaroid:").strip()
        else:
            return
        response = self.sugaroid.parse(msg)
        await self.client.room_send(
            room.room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": str(response)
            }
        )
