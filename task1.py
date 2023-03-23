class SomeModel:
    def predict(self, message: str) -> float:
        return 0.5


def predict_message_mood(
    message: str,
    model: SomeModel,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    pred = model.predict(message)
    ans = ''
    if pred < bad_thresholds:
        ans = "неуд"
    elif pred > good_thresholds:
        ans = "отл"
    else:
        ans = "норм"
    return ans
