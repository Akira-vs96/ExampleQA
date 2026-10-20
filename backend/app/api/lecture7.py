from fastapi import APIRouter, HTTPException

from app.schemas import LectureTopic, LessonStep
from lecture7.content import DEBUG_WORKFLOW, TOPICS


router = APIRouter(tags=["lecture 7"])


@router.get("/lecture7/topics", response_model=list[LectureTopic])
def list_topics() -> list[LectureTopic]:
    return [LectureTopic(**topic) for topic in TOPICS]


@router.get("/lecture7/topics/{topic_id}", response_model=LectureTopic)
def get_topic(topic_id: int) -> LectureTopic:
    for topic in TOPICS:
        if topic["id"] == topic_id:
            return LectureTopic(**topic)
    raise HTTPException(status_code=404, detail="Мұндай дәріс тақырыбы табылмады.")


@router.get("/guide", response_model=list[LessonStep], deprecated=True)
def get_guide() -> list[LessonStep]:
    return [
        LessonStep(id=index, title=title, description=description, action="Орындалды деп белгілеу")
        for index, (title, description) in enumerate(DEBUG_WORKFLOW, start=1)
    ]
