from ultralytics import YOLO

source = '/root/autodl-tmp/Station/back/upload/videos/1.mov'

model = YOLO('/root/autodl-tmp/runs/detect/train3/weights/best.pt')
results = model.predict(source=source, stream=True, save_txt=True)
for result in results:
    print(result.tojson())
    # print(result.names)
    # print(result.probs)

