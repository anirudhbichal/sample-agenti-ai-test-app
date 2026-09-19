from typing import List

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


app = FastAPI(title="Message Processor API")


class MessageCreate(BaseModel):
	content: str


class Message(MessageCreate):
	id: int


messages: List[Message] = []
next_id = 1


@app.get("/")
def root():
	return {"message": "Message Processor API is running"}


@app.get("/messages", response_model=List[Message])
def get_messages():
	return messages


@app.get("/messages/{message_id}", response_model=Message)
def get_message(message_id: int):
	for message in messages:
		if message.id == message_id:
			return message
	raise HTTPException(status_code=404, detail="Message not found")


@app.post("/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
def create_message(message_data: MessageCreate):
	global next_id
	message = Message(id=next_id, content=message_data.content)
	messages.append(message)
	next_id += 1
	return message


@app.put("/messages/{message_id}", response_model=Message)
def update_message(message_id: int, message_data: MessageCreate):
	for index, message in enumerate(messages):
		if message.id == message_id:
			updated_message = Message(id=message_id, content=message_data.content)
			messages[index] = updated_message
			return updated_message
	raise HTTPException(status_code=404, detail="Message not found")


@app.delete("/messages/{message_id}")
def delete_message(message_id: int):
	for index, message in enumerate(messages):
		if message.id == message_id:
			messages.pop(index)
			return {"detail": "Message deleted"}
	raise HTTPException(status_code=404, detail="Message not found")


if __name__ == "__main__":
	import uvicorn

	uvicorn.run(app, host="0.0.0.0", port=8000)
