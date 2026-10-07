from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, HRFlowable

ROOT = Path(r"C:\Users\abhay\Driver_Monitoring")
OUT = ROOT / "output" / "pdf" / "driver_drowsiness_project_task_6_75_percent_report.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
NAVY=colors.HexColor("#14283D"); BLUE=colors.HexColor("#1D5D9B"); TEAL=colors.HexColor("#0F766E")
PALE=colors.HexColor("#F4F8FB"); INK=colors.HexColor("#243746"); MUTED=colors.HexColor("#607080")
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name="ct",parent=styles["Title"],fontName="Helvetica-Bold",fontSize=23,leading=28,textColor=NAVY,alignment=1,spaceAfter=10))
styles.add(ParagraphStyle(name="cs",parent=styles["Normal"],fontSize=12,leading=17,textColor=INK,alignment=1,spaceAfter=7))
styles.add(ParagraphStyle(name="h1x",parent=styles["Heading1"],fontName="Helvetica-Bold",fontSize=15,leading=19,textColor=NAVY,spaceBefore=4,spaceAfter=8))
styles.add(ParagraphStyle(name="h2x",parent=styles["Heading2"],fontName="Helvetica-Bold",fontSize=11,leading=14,textColor=BLUE,spaceBefore=7,spaceAfter=5))
styles.add(ParagraphStyle(name="bx",parent=styles["BodyText"],fontSize=9.2,leading=13.4,textColor=INK,spaceAfter=6))
styles.add(ParagraphStyle(name="sx",parent=styles["BodyText"],fontSize=8,leading=11,textColor=MUTED,spaceAfter=4))
styles.add(ParagraphStyle(name="co",parent=styles["BodyText"],fontSize=9,leading=13,textColor=INK,backColor=PALE,borderColor=colors.HexColor("#D7E3ED"),borderWidth=.7,borderPadding=8,spaceBefore=5,spaceAfter=8))
styles.add(ParagraphStyle(name="cl",parent=styles["Normal"],fontName="Helvetica-Bold",fontSize=8.5,leading=11,textColor=BLUE,spaceBefore=5,spaceAfter=3))
styles.add(ParagraphStyle(name="code",parent=styles["Code"],fontName="Courier",fontSize=6.7,leading=8.2,textColor=colors.HexColor("#17324D"),backColor=colors.HexColor("#F7FAFC"),borderColor=colors.HexColor("#D7E3ED"),borderWidth=.5,borderPadding=7,spaceAfter=7))
def P(t,s="bx"): return Paragraph(t,styles[s])
def tab(data,widths,font=8):
    t=Table(data,colWidths=widths,repeatRows=1,hAlign="LEFT")
    c=[("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),("BACKGROUND",(0,0),(-1,0),NAVY),("TEXTCOLOR",(0,0),(-1,0),colors.white),("FONTNAME",(0,1),(-1,-1),"Helvetica"),("FONTSIZE",(0,0),(-1,-1),font),("TEXTCOLOR",(0,1),(-1,-1),INK),("VALIGN",(0,0),(-1,-1),"TOP"),("GRID",(0,0),(-1,-1),.35,colors.HexColor("#C7D5E0")),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]
    for r in range(2,len(data),2): c.append(("BACKGROUND",(0,r),(-1,r),PALE))
    t.setStyle(TableStyle(c)); return t
def code(label,text): return [P(label,"cl"),Preformatted(text.strip("\n"),styles["code"])]
def hf(canvas,doc):
    canvas.saveState(); w,h=A4; canvas.setFillColor(NAVY); canvas.rect(0,h-13*mm,w,13*mm,fill=1,stroke=0); canvas.setFont("Helvetica-Bold",8); canvas.setFillColor(colors.white); canvas.drawString(16*mm,h-8.5*mm,"CSE411  |  COMPUTER VISION  |  PROJECT TASK 6"); canvas.setFont("Helvetica",8); canvas.setFillColor(MUTED); canvas.drawString(16*mm,10*mm,"Driver Drowsiness Detection System  ·  Team 25"); canvas.drawRightString(w-16*mm,10*mm,f"Page {doc.page}"); canvas.restoreState()
frame=Frame(16*mm,16*mm,A4[0]-32*mm,A4[1]-37*mm,id="f",leftPadding=0,rightPadding=0,topPadding=3*mm,bottomPadding=0)
doc=BaseDocTemplate(str(OUT),pagesize=A4,leftMargin=16*mm,rightMargin=16*mm,topMargin=18*mm,bottomMargin=16*mm,title="Project Task 6 - Driver Drowsiness Detection",author="Team 25")
doc.addPageTemplates([PageTemplate(id="p",frames=frame,onPage=hf)])
S=[]
S += [Spacer(1,20*mm),P("CSE411 — COMPUTER VISION","cs"),P("Project Task 6","ct"),P("Implementation — Part 3","cs"),Spacer(1,8*mm),HRFlowable(width="65%",thickness=2,color=TEAL,hAlign="CENTER"),Spacer(1,10*mm),P("Driver Drowsiness Detection System Using Computer Vision","cs"),Spacer(1,12*mm)]
S.append(tab([[P("Project detail","sx"),P("Information","sx")],[P("Team Number","bx"),P("25","bx")],[P("Team Members","bx"),P("Vangara Sridhar — 2023BCS0106<br/>Suragouni Sahithi — 2023BCS0070<br/>Vatte Ramya Sri — 2023BCS0208<br/>Abhay Devanand Sawale — 2023BCS0046","bx")],[P("Continuation of","bx"),P("Project Task 5 — Implementation, Part 2","bx")],[P("Report status","bx"),P("Approximately 75% project milestone","bx")]], [42*mm,122*mm],9)); S.append(Spacer(1,12*mm)); S.append(P("This report documents the next implementation milestone using the existing Driver_Monitoring project as the reference. The repository source code is intentionally untouched for this submission. Code shown in the Task 6 design appendix is labelled as proposed report-level implementation code.","co")); S.append(PageBreak())
S += [P("1. Task 6 Objective and Completion Position","h1x"),P("The Task 6 brief asks the team to complete approximately 75% of the proposed work, integrate completed modules into a working prototype, demonstrate current outputs, and clearly state the remaining 25%. The Task 5 milestone already established the functioning camera → API → model → frontend path. Task 6 extends that foundation with classical computer-vision signals that are relevant to drowsiness and live video.")]
S.append(tab([[P("Milestone","sx"),P("Evidence / position","sx")],[P("Task 1–3 foundation","bx"),P("Problem definition, literature gap, architecture, YOLO methodology, and consecutive-frame alarm concept are documented in earlier submissions.","bx")],[P("Task 4–5 foundation","bx"),P("The repository contains a FastAPI backend, Next.js webcam frontend, YOLO classifier, validation, inference parsing, session statistics, and five-second alarm logic.","bx")],[P("Task 6 expansion","bx"),P("HOG, optical-flow motion, and Sobel/thresholding/morphology are specified as a coherent feature pipeline with API exposure and validation steps.","bx")],[P("Report boundary","bx"),P("The project source remains unchanged exactly as requested. The new code in this report is a proposed implementation appendix for the next controlled code change.","bx")]], [37*mm,127*mm],8.2))
S += [P("1.1 Why these components fit the project","h2x"),P("HOG is directly connected to the computer-vision syllabus and can describe local gradient structure around a face or eye region. Optical flow is a natural match for the current one-frame-per-second live monitoring loop because it adds motion information between consecutive frames. Sobel edges, thresholding, and morphology provide an interpretable classical preprocessing branch that can expose boundaries and clean binary regions before model inference."),P("The design intentionally keeps YOLO as the main learned classifier. The classical features act as additional visual evidence and diagnostics rather than silently replacing the trained model.","co"),P("2. Integrated Task 6 Architecture","h1x"),P("The proposed Task 6 pipeline preserves the working Task 5 data path and inserts a parallel classical-CV analysis branch. This makes the milestone explainable: the system still returns the trained model prediction, while the API also reports the visual feature measurements used for monitoring and later evaluation.")]
S.append(tab([[P("Stage","sx"),P("Component","sx"),P("Output","sx")],[P("1. Capture","bx"),P("Camera.jsx captures a ready JPEG frame","bx"),P("Frame t","bx")],[P("2. Decode","bx"),P("FastAPI validation and OpenCV decode","bx"),P("BGR image","bx")],[P("3. Classical CV","bx"),P("HOG + Sobel magnitude + Otsu threshold + morphology","bx"),P("Shape, edge, region descriptors","bx")],[P("4. Temporal branch","bx"),P("Optical flow between previous and current frame","bx"),P("Motion magnitude","bx")],[P("5. Learned inference","bx"),P("YOLO classification through inference.py","bx"),P("Label and probabilities","bx")],[P("6. Response","bx"),P("Frontend streak/alarm + JSON diagnostics","bx"),P("Status + CV metadata","bx")]], [30*mm,82*mm,52*mm],7.8))
S.append(PageBreak())
S += [P("2.1 Extended response design","h1x"),P("The additional measurements should be exposed as metadata so they can be inspected during demonstrations and used in later experiments. They should not be treated as a medical or safety guarantee; the system remains an assistive prototype.")]
S.append(Preformatted('''{
  "success": true,
  "prediction": {"label": "Drowsy", "confidence": 0.91,
    "cv_features": {
      "hog": {"enabled": true, "feature_length": 8100},
      "optical_flow": {"available": true, "mean_magnitude": 0.18},
      "sobel": {"edge_density": 0.21, "threshold": "otsu", "morphology": true}
    }
  }
}''',styles["code"]))
S += [P("3. Existing Prototype Evidence","h1x"),P("The following evidence is carried forward from the repository and the Task 5 report. It demonstrates that the base prototype is already integrated and provides a stable place for the Task 6 CV branch.")]
S.append(tab([[P("Check","sx"),P("Observed result","sx"),P("Meaning","sx")],[P("GET /health","bx"),P("healthy; model_loaded = true","bx"),P("Backend starts and loads a checkpoint.","bx")],[P("POST /predict smoke test","bx"),P("Drowsy; confidence about 0.91; severity 2","bx"),P("Image decoding, inference, and response formatting work end to end.","bx")],[P("Model classes","bx"),P("Alert, Drowsy, Low_Vigilant, Non_Drowsy","bx"),P("Configured checkpoint is a drowsiness classifier.","bx")],[P("Frontend lint / build","bx"),P("Passed","bx"),P("No lint errors; Next.js production compilation succeeds.","bx")],[P("Alarm logic","bx"),P("Five seconds of continuous Drowsy results","bx"),P("A single paused frame cannot trigger the temporal alarm.","bx")]], [43*mm,55*mm,66*mm],7.9))
S += [P("3.1 Current limitations carried into Task 6","h2x"),P("The current classifier predicts from an image, while drowsiness is temporal. The optical-flow branch supplies motion evidence, but it does not by itself measure eye closure. HOG and edge features can be affected by illumination, glasses, pose, and background clutter. These limitations must be measured in the final evaluation rather than hidden behind a single accuracy number.")]
S.append(tab([[P("Risk","sx"),P("Control","sx")],[P("False alarms from one frame","bx"),P("Keep consecutive-frame timing and use temporal smoothing in the final milestone.","bx")],[P("Background/camera motion","bx"),P("Normalize the ROI, report flow as metadata, and test stationary versus moving-camera conditions.","bx")],[P("Lighting sensitivity","bx"),P("Use grayscale normalization and compare edge/HOG distributions across lighting conditions.","bx")],[P("API latency","bx"),P("Measure processing time for each branch and keep diagnostics lightweight.","bx")]], [55*mm,109*mm],8))
S.append(PageBreak())
S += [P("4. Code Appendix A — Existing Project Components","h1x"),P("These excerpts are taken from the current project folder and are included to connect the report to the actual implementation. They are not changes made for this PDF.")]
S += code("A. Existing OpenCV preprocessing — backend/app/services/image_processing.py",'''def preprocess_for_yolo(image: np.ndarray,
                        target_size: Tuple[int, int] = (640, 640)) -> np.ndarray:
    # Convert BGR to RGB (YOLO expects RGB)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return img_rgb''')
S += code("B. Existing inference path — backend/app/services/inference.py",'''model = model_manager.get_model()
img_rgb = preprocess_for_yolo(image)
results = model.predict(img_rgb, conf_threshold=conf_threshold)
result = results[0]
probs = result.probs
predicted_class_idx = int(probs.top1)
confidence = float(probs.top1conf)
class_name = result.names[predicted_class_idx]
prediction = format_prediction(class_name, confidence)''')
S += code("C. Existing frontend temporal alarm — frontend/app/page.jsx",'''const DROWSY_ALARM_SECONDS = 5;
if (prediction.status === 'drowsy') {
  if (drowsySinceRef.current === null) drowsySinceRef.current = now;
  const elapsedSeconds = (now - drowsySinceRef.current) / 1000;
  setDrowsyStreak(Math.floor(elapsedSeconds));
  if (elapsedSeconds >= DROWSY_ALARM_SECONDS) startAlarm();
} else {
  drowsySinceRef.current = null;
  setDrowsyStreak(0);
  stopAlarm();
}''')
S.append(PageBreak())
S += [P("5. Code Appendix B — Task 6 CV Components","h1x"),P("The following code is the required report-level design for Task 6. It is intentionally included in the PDF rather than written into the repository, following the instruction to leave the codebase untouched. The intended new module is backend/app/services/cv_features.py.")]
S += code("B1. HOG, Sobel, thresholding, morphology — proposed cv_features.py",'''import cv2
import numpy as np

def compute_hog(image: np.ndarray) -> dict:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (128, 128))
    descriptor = cv2.HOGDescriptor(_winSize=(128,128), _blockSize=(16,16),
        _blockStride=(8,8), _cellSize=(8,8), _nbins=9)
    values = descriptor.compute(gray)
    return {"enabled": True, "feature_length": int(values.size),
            "mean": float(values.mean()), "std": float(values.std())}

def compute_sobel_features(image: np.ndarray) -> dict:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    magnitude = cv2.magnitude(gx, gy)
    magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
    _, binary = cv2.threshold(magnitude.astype(np.uint8), 0, 255,
                               cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.ones((3, 3), np.uint8)
    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    cleaned = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
    return {"edge_density": float(np.mean(cleaned > 0)),
            "threshold": "otsu", "morphology": True}''')
S += code("B2. Optical-flow tracker — proposed cv_features.py",'''def compute_optical_flow(previous_gray, frame: np.ndarray):
    current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if previous_gray is None:
        return current_gray, {"available": False, "mean_magnitude": 0.0}
    flow = cv2.calcOpticalFlowFarneback(
        previous_gray, current_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    return current_gray, {"available": True,
        "mean_magnitude": float(np.mean(magnitude)),
        "max_magnitude": float(np.max(magnitude))}''')
S.append(P("Implementation note: an optical-flow tracker must keep previous-frame state per monitoring session or worker. It must reset when monitoring stops, when the camera changes, or when a frame is missing.","co"))
S += [P("5.1 Proposed inference integration","h2x")]
S += code("B3. Add-on metadata at the inference boundary — proposed",'''cv = {
    "hog": compute_hog(image),
    "sobel": compute_sobel_features(image),
    "optical_flow": flow_info,
}
prediction["cv_features"] = cv
return prediction''')
S.append(PageBreak())
S += [P("6. Demonstration and Validation Plan","h1x"),P("The Task 6 demonstration should show both the existing application and the new CV signals. The goal is not merely to calculate features, but to prove that each component is connected to a visible or measurable output.")]
S.append(tab([[P("Test","sx"),P("Procedure","sx"),P("Expected evidence","sx")],[P("HOG extraction","bx"),P("Send a valid frame through the feature service and record descriptor length and summary statistics.","bx"),P("JSON contains hog.enabled=true and non-zero feature length.","bx")],[P("Sobel pipeline","bx"),P("Run gradient magnitude, Otsu threshold, opening, and closing.","bx"),P("JSON contains edge density and morphology=true.","bx")],[P("Optical flow","bx"),P("Send consecutive frames with head movement and then identical frames.","bx"),P("Movement has higher magnitude than identical frames.","bx")],[P("Temporal alarm","bx"),P("Run live monitoring with sustained Drowsy predictions for at least five seconds.","bx"),P("Streak reaches threshold; audio/tone and visual alarm appear.","bx")],[P("Reset behavior","bx"),P("Stop monitoring or send a non-drowsy result after an alarm.","bx"),P("Alarm stops, streak resets, and flow state is cleared.","bx")],[P("Robustness","bx"),P("Repeat under low light, glasses, different subjects, and camera movement.","bx"),P("Record latency, false alarms, missed alarms, and feature changes.","bx")]], [31*mm,75*mm,48*mm],7.6))
S += [P("6.1 Demonstration outputs","h2x"),P("Include one screenshot of the working frontend, one backend JSON response containing cv_features, and a small table of consecutive-frame measurements. A single image with closed eyes is not enough to prove a five-second alarm because the current alarm is temporal and needs continuous live monitoring."),tab([[P("Frame","sx"),P("Status","sx"),P("Flow","sx"),P("Alarm","sx")],[P("t−2","bx"),P("Drowsy","bx"),P("0.14","bx"),P("off","bx")],[P("t−1","bx"),P("Drowsy","bx"),P("0.18","bx"),P("off","bx")],[P("t","bx"),P("Drowsy","bx"),P("0.16","bx"),P("on after threshold","bx")]], [30*mm,50*mm,45*mm,50*mm],8),P("The numeric values above are an example of the intended reporting format, not a claim that these exact optical-flow values were produced by the untouched repository.","sx")]
S += [P("7. Remaining 25% of the Project","h1x"),P("After the Task 6 design and integration milestone, the final 25% should concentrate on validation, direct eye-state measurement, deployment hardening, and final documentation.")]
S.append(tab([[P("Remaining work","sx"),P("What must be completed","sx"),P("Completion evidence","sx")],[P("Formal evaluation","bx"),P("Subject/video-level held-out split; accuracy, precision, recall, F1, confusion matrix, per-class results.","bx"),P("Reproducible evaluation script and tables.","bx")],[P("Direct eye closure","bx"),P("Add facial landmarks or an eye-state detector and measure continuous closure / blink duration.","bx"),P("Eye-region evidence tied to alarm decision.","bx")],[P("Temporal robustness","bx"),P("Tune smoothing, missing-frame handling, thresholds, and reset behavior across conditions.","bx"),P("Scenario matrix with false/missed alarms.","bx")],[P("Deployment validation","bx"),P("Validate production env vars, CORS, cold starts, model availability, timeout, and connectivity.","bx"),P("Production smoke test and checklist.","bx")],[P("Safety UX/docs","bx"),P("Test alarm.mp3, browser audio permissions, mute/reset, safety disclaimer, and final instructions.","bx"),P("Final demo, README, limitations, reproducibility notes.","bx")]], [40*mm,89*mm,46*mm],7.7))
S.append(P("Priority recommendation: complete formal evaluation and direct eye-closure measurement first. Optical flow and HOG strengthen the computer-vision milestone, but they should not be presented as a replacement for explicit eye-state measurement when the requirement is specifically ‘eyes closed for five seconds’.","co"))
S += [P("8. Conclusion","h1x"),P("Task 6 advances the Driver Drowsiness Detection System from a connected model-serving prototype toward a more complete computer-vision system. The existing camera, validation, YOLO inference, frontend feedback, and temporal alarm path remain the foundation. HOG, optical-flow, Sobel, thresholding, and morphology add interpretable spatial and temporal evidence and expose it as structured diagnostics."),P("The source repository has not been changed for this report. The implementation snippets are supplied in the PDF so the team can review, discuss, and apply them in a later controlled code change. The project should be considered approximately 75% complete only after the feature branch is implemented and the validation plan is executed; the final 25% is the evaluation and reliability work listed above.","co"),P("Project files referenced","h2x"),P("backend/app/services/image_processing.py · backend/app/services/inference.py · backend/app/routes/predict.py · backend/app/models/model.py · frontend/app/page.jsx · frontend/components/Camera.jsx · ml_pipeline/train.py","sx")]
doc.build(S)
print(OUT)
