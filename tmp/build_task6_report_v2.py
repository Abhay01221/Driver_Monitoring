from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, HRFlowable

ROOT = Path(r"C:\Users\abhay\Driver_Monitoring")
OUT = ROOT / "output" / "pdf" / "driver_drowsiness_project_task_6_75_percent_report.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)
NAVY=colors.HexColor('#14283D'); BLUE=colors.HexColor('#1D5D9B'); TEAL=colors.HexColor('#0F766E'); PALE=colors.HexColor('#F4F8FB'); INK=colors.HexColor('#243746'); MUTED=colors.HexColor('#607080'); GOLD=colors.HexColor('#B45309')
ss=getSampleStyleSheet()
ss.add(ParagraphStyle(name='TitleX',parent=ss['Title'],fontName='Helvetica-Bold',fontSize=23,leading=28,textColor=NAVY,alignment=1,spaceAfter=8))
ss.add(ParagraphStyle(name='SubX',parent=ss['Normal'],fontSize=11.5,leading=16,textColor=INK,alignment=1,spaceAfter=6))
ss.add(ParagraphStyle(name='H1X',parent=ss['Heading1'],fontName='Helvetica-Bold',fontSize=15,leading=19,textColor=NAVY,spaceBefore=3,spaceAfter=8))
ss.add(ParagraphStyle(name='H2X',parent=ss['Heading2'],fontName='Helvetica-Bold',fontSize=11.2,leading=14,textColor=BLUE,spaceBefore=7,spaceAfter=5))
ss.add(ParagraphStyle(name='BodyX',parent=ss['BodyText'],fontSize=9.1,leading=13.2,textColor=INK,spaceAfter=6))
ss.add(ParagraphStyle(name='SmallX',parent=ss['BodyText'],fontSize=7.8,leading=10.5,textColor=MUTED,spaceAfter=4))
ss.add(ParagraphStyle(name='CallX',parent=ss['BodyText'],fontSize=9,leading=13,textColor=INK,backColor=PALE,borderColor=colors.HexColor('#D3E0EA'),borderWidth=.7,borderPadding=8,spaceBefore=5,spaceAfter=8))
ss.add(ParagraphStyle(name='CodeLabelX',parent=ss['Normal'],fontName='Helvetica-Bold',fontSize=8.5,leading=11,textColor=BLUE,spaceBefore=5,spaceAfter=3))
ss.add(ParagraphStyle(name='CodeX',parent=ss['Code'],fontName='Courier',fontSize=6.6,leading=8.1,textColor=colors.HexColor('#17324D'),backColor=colors.HexColor('#F7FAFC'),borderColor=colors.HexColor('#D3E0EA'),borderWidth=.5,borderPadding=7,spaceAfter=7))
def P(t,s='BodyX'): return Paragraph(t,ss[s])
def T(rows,widths,font=8):
    x=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
    c=[('BACKGROUND',(0,0),(-1,0),NAVY),('TEXTCOLOR',(0,0),(-1,0),colors.white),('FONTNAME',(0,0),(-1,0),'Helvetica-Bold'),('FONTNAME',(0,1),(-1,-1),'Helvetica'),('FONTSIZE',(0,0),(-1,-1),font),('TEXTCOLOR',(0,1),(-1,-1),INK),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),.35,colors.HexColor('#C7D5E0')),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]
    for r in range(2,len(rows),2): c.append(('BACKGROUND',(0,r),(-1,r),PALE))
    x.setStyle(TableStyle(c)); return x
def code(label,text): return [P(label,'CodeLabelX'),Preformatted(text.strip(),ss['CodeX'])]
def hf(c,d):
    c.saveState(); w,h=A4; c.setFillColor(NAVY); c.rect(0,h-13*mm,w,13*mm,fill=1,stroke=0); c.setFillColor(colors.white); c.setFont('Helvetica-Bold',8); c.drawString(16*mm,h-8.5*mm,'CSE411  |  COMPUTER VISION  |  PROJECT TASK 6'); c.setFillColor(MUTED); c.setFont('Helvetica',8); c.drawString(16*mm,10*mm,'Driver Drowsiness Detection System  ·  Team 25'); c.drawRightString(w-16*mm,10*mm,f'Page {d.page}'); c.restoreState()
fr=Frame(16*mm,16*mm,A4[0]-32*mm,A4[1]-37*mm,id='f',leftPadding=0,rightPadding=0,topPadding=3*mm,bottomPadding=0)
doc=BaseDocTemplate(str(OUT),pagesize=A4,leftMargin=16*mm,rightMargin=16*mm,topMargin=18*mm,bottomMargin=16*mm,title='Driver Drowsiness Detection - Project Task 6',author='Team 25')
doc.addPageTemplates([PageTemplate(id='main',frames=fr,onPage=hf)])
S=[]
# Cover
S += [Spacer(1,16*mm),P('CSE411 — COMPUTER VISION','SubX'),P('Project Task 6','TitleX'),P('Implementation — Part 3','SubX'),Spacer(1,7*mm),HRFlowable(width='65%',thickness=2,color=TEAL,hAlign='CENTER'),Spacer(1,9*mm),P('Driver Drowsiness Detection System Using Computer Vision','SubX'),Spacer(1,9*mm)]
S.append(T([[P('Project detail','SmallX'),P('Information','SmallX')],[P('Team Number','BodyX'),P('25','BodyX')],[P('Team Members','BodyX'),P('Vangara Sridhar — 2023BCS0106<br/>Suragouni Sahithi — 2023BCS0070<br/>Vatte Ramya Sri — 2023BCS0208<br/>Abhay Devanand Sawale — 2023BCS0046','BodyX')],[P('Continuation of','BodyX'),P('Project Task 5 — Implementation, Part 2','BodyX')],[P('Milestone','BodyX'),P('Approximately 75% of proposed project work','BodyX')]], [42*mm,122*mm],8.8)); S.append(Spacer(1,9*mm)); S.append(P('This report continues the earlier Task 1–5 submissions. It documents the current working prototype, the Task 6 computer-vision modules, their intended integration, current evidence, limitations, and the remaining 25%. The source codebase is intentionally unchanged for this report.', 'CallX')); S.append(PageBreak())
# 1
S += [P('1. Introduction and Task 6 Objective','H1X'),P('Driver drowsiness is a gradual condition that cannot always be represented reliably by one isolated image. The project therefore combines image classification with a temporal decision rule. The previous milestone connected the camera, FastAPI backend, trained YOLO classifier, frontend result display, and five-second alarm logic into one runnable prototype.'),P('Project Task 6 requires the team to complete approximately 75% of the proposed work, integrate completed modules into a working prototype, demonstrate outputs, and state the unfinished 25%. The next step is to strengthen the computer-vision pipeline with interpretable classical features while preserving the current application flow.')]
S.append(T([[P('Area','SmallX'),P('Task 5 position','SmallX'),P('Task 6 position','SmallX')],[P('Input','BodyX'),P('Webcam frame captured in the browser and uploaded as an image.','BodyX'),P('Keep the same capture path and use each frame for spatial and temporal CV analysis.','BodyX')],[P('Preprocessing','BodyX'),P('OpenCV decode and BGR-to-RGB conversion.','BodyX'),P('Add HOG, Sobel gradients, histogram thresholding, and morphology as report-level CV components.','BodyX')],[P('Temporal reasoning','BodyX'),P('Five-second continuous Drowsy timer in frontend.','BodyX'),P('Add optical-flow magnitude between consecutive frames and retain the alarm timer.','BodyX')],[P('Model','BodyX'),P('YOLO classification checkpoint with drowsiness classes.','BodyX'),P('Keep YOLO as the main classifier; expose CV metadata beside prediction probabilities.','BodyX')],[P('Validation','BodyX'),P('Health check, prediction smoke test, lint, and build evidence.','BodyX'),P('Add feature-specific checks, latency observations, and robustness scenarios.','BodyX')]], [31*mm,72*mm,61*mm],7.8))
S += [P('1.1 Scope boundary','H2X'),P('Because the request explicitly says not to change the codebase, this PDF includes the required Task 6 module code as a documented implementation appendix. The snippets are marked proposed and are not claimed as files already present in the repository. This keeps the report technically honest while giving the team the code needed for the next controlled implementation step.'),P('The completed system remains an assistive prototype and must not be treated as a replacement for safe driving, professional medical assessment, or a certified vehicle safety system.','CallX')]
# 2
S.append(PageBreak()); S += [P('2. Existing Integrated System','H1X'),P('The current project is organized as a frontend, backend, and machine-learning pipeline. A browser camera captures a frame, the frontend sends it through the API client, FastAPI validates and decodes the upload, the inference service calls the loaded YOLO model, and the response is rendered in the detection result interface. The frontend also counts session frames and tracks continuous drowsiness for the alarm.')]
S.append(T([[P('Stage','SmallX'),P('Current component','SmallX'),P('Current output','SmallX')],[P('Camera capture','BodyX'),P('frontend/components/Camera.jsx','BodyX'),P('JPEG frame from the browser camera.','BodyX')],[P('API request','BodyX'),P('frontend/lib/api.js','BodyX'),P('Multipart upload with timeout and readable errors.','BodyX')],[P('Validation/decode','BodyX'),P('backend/app/routes/predict.py + image_processing.py','BodyX'),P('Accepted image decoded into an OpenCV array.','BodyX')],[P('Inference','BodyX'),P('backend/app/models/model.py + services/inference.py','BodyX'),P('Class label, confidence, and all class probabilities.','BodyX')],[P('Feedback','BodyX'),P('frontend/app/page.jsx + DetectionResult.jsx','BodyX'),P('Status card, confidence, session statistics, and streak.','BodyX')],[P('Alarm','BodyX'),P('Frontend temporal timer and optional alarm.mp3','BodyX'),P('Alarm after five seconds of continuous Drowsy results.','BodyX')]], [32*mm,72*mm,60*mm],7.8))
S += [P('2.1 Task 6 architecture','H2X'),P('The proposed extension adds a classical computer-vision branch between image decoding and the final response. HOG describes local gradients, Sobel and morphology describe edges and cleaned regions, and optical flow compares the current frame with the previous frame. These outputs are returned as diagnostics so the feature work is observable rather than calculated and discarded.')]
S.append(Preformatted('''Camera frame t
      |
      +--> OpenCV decode / grayscale
      |        +--> HOG descriptor
      |        +--> Sobel magnitude -> Otsu threshold -> morphology
      |
      +--> frame t + previous frame t-1 -> Farneback optical flow
      |
      +--> YOLO classification -> label + confidence + probabilities
                              |
                              +--> JSON response + frontend streak/alarm''',ss['CodeX']))
S.append(P('The YOLO prediction remains the primary learned decision. The classical branch supplies additional evidence and a stronger syllabus connection; it should only influence the final alarm after testing and calibration.','CallX'))
# 3
S.append(PageBreak()); S += [P('3. Task 6 Computer-Vision Components','H1X'),P('Three genuine computer-vision additions are documented for this milestone. Together they cover gradient-based descriptors, motion analysis, edge detection, thresholding, segmentation, and morphological filtering.')]
S.append(T([[P('Component','SmallX'),P('Purpose in this project','SmallX'),P('Output used by the system','SmallX')],[P('HOG','BodyX'),P('Represent local gradient orientation patterns around the driver or a selected face/eye region.','BodyX'),P('Feature length, mean, and standard deviation in cv_features metadata.','BodyX')],[P('Optical flow','BodyX'),P('Compare consecutive monitoring frames to estimate motion and stability.','BodyX'),P('Mean/max motion magnitude and availability flag.','BodyX')],[P('Sobel + thresholding','BodyX'),P('Extract horizontal/vertical gradients, combine them into edge magnitude, and obtain a binary map using Otsu thresholding.','BodyX'),P('Edge density and selected threshold method.','BodyX')],[P('Morphology','BodyX'),P('Remove small isolated regions and close small gaps in the binary edge map.','BodyX'),P('Cleaned binary-region density and morphology flag.','BodyX')]], [34*mm,78*mm,52*mm],7.7))
S += [P('3.1 HOG feature extraction','H2X'),P('Histogram of Oriented Gradients divides an image into local cells, estimates gradient directions, and aggregates them into normalized blocks. In this project it can be applied to a fixed-size driver or face region. The feature summary is exposed in the response so the team can verify that HOG is actually calculated and not silently ignored.'),P('3.2 Optical flow for live monitoring','H2X'),P('The frontend already produces a sequence of frames approximately one second apart during live monitoring. Farneback optical flow can estimate the displacement field between consecutive grayscale images. A low value may indicate a stable frame, while larger values can reflect head movement, camera movement, or background changes. It is therefore an additional signal, not a direct drowsiness label.')]
S.append(P('The tracker must reset when monitoring stops, when the camera changes, or when a frame is missing. State should be scoped to a monitoring session so one user’s previous frame cannot contaminate another session.','CallX'))
# 4
S.append(PageBreak()); S += [P('4. Implementation Appendix — Proposed CV Module','H1X'),P('The following code is included in the report as the Task 6 implementation design. The intended module is backend/app/services/cv_features.py. It is not written into the codebase in accordance with the instruction to leave all source files untouched.')]
S += code('A. HOG and Sobel/threshold/morphology — proposed cv_features.py','''import cv2
import numpy as np

def compute_hog(image: np.ndarray) -> dict:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (128, 128))
    descriptor = cv2.HOGDescriptor(
        _winSize=(128, 128), _blockSize=(16, 16),
        _blockStride=(8, 8), _cellSize=(8, 8), _nbins=9
    )
    values = descriptor.compute(gray)
    return {"enabled": True,
            "feature_length": int(values.size),
            "mean": float(values.mean()),
            "std": float(values.std())}

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
S += code('B. Optical-flow tracker — proposed cv_features.py','''def compute_optical_flow(previous_gray, frame: np.ndarray):
    current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if previous_gray is None:
        return current_gray, {"available": False, "mean_magnitude": 0.0}
    flow = cv2.calcOpticalFlowFarneback(
        previous_gray, current_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
    )
    magnitude, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    return current_gray, {"available": True,
        "mean_magnitude": float(np.mean(magnitude)),
        "max_magnitude": float(np.max(magnitude))}''')
# 5
S.append(PageBreak()); S += [P('5. Inference and API Integration Design','H1X'),P('The existing inference function already returns a structured prediction containing the label, confidence, and class probabilities. The Task 6 extension should attach a cv_features object to that same prediction instead of changing the existing response contract. This keeps the frontend compatible while making the additional analysis available for demonstration and future evaluation.')]
S += code('C. Proposed inference metadata integration','''# After the existing YOLO prediction has been created:
cv_features = {
    "hog": compute_hog(image),
    "sobel": compute_sobel_features(image),
    "optical_flow": flow_info,
}
prediction["cv_features"] = cv_features
return prediction''')
S.append(Preformatted('''{
  "success": true,
  "prediction": {
    "label": "Drowsy",
    "confidence": 0.91,
    "status": "drowsy",
    "all_probs": {"Alert": 0.03, "Drowsy": 0.91,
                  "Low_Vigilant": 0.04, "Non_Drowsy": 0.02},
    "cv_features": {
      "hog": {"enabled": true, "feature_length": 8100},
      "optical_flow": {"available": true, "mean_magnitude": 0.18},
      "sobel": {"edge_density": 0.21, "threshold": "otsu",
                "morphology": true}
    }
  }
}''',ss['CodeX']))
S += [P('5.1 Existing temporal alarm connection','H2X'),P('The current frontend starts timing when the prediction status becomes drowsy and resets the timer when the result is no longer drowsy. After the configured five-second duration, the alarm begins. This is important for the project requirement: one still image with closed eyes cannot prove five seconds of continuous closure; a live sequence is required.')]
S.append(T([[P('Condition','SmallX'),P('System response','SmallX')],[P('Drowsy prediction begins','BodyX'),P('Store the start time and increase the displayed drowsy streak.','BodyX')],[P('Drowsy persists for five seconds','BodyX'),P('Start the optional alarm.mp3 or browser tone fallback and show visual alarm feedback.','BodyX')],[P('Alert / Non-Drowsy result','BodyX'),P('Reset the streak and stop the alarm.','BodyX')],[P('Monitoring stopped','BodyX'),P('Clear alarm state and reset temporal / optical-flow session state.','BodyX')]], [60*mm,104*mm],8))
# 6
S.append(PageBreak()); S += [P('6. Implementation Evidence and Results','H1X'),P('The Task 5 report recorded the working baseline that Task 6 builds on. These results are repository-grounded and are separated from the proposed Task 6 feature code because the source files were not modified for this submission.')]
S.append(T([[P('Test / check','SmallX'),P('Observed result','SmallX'),P('Interpretation','SmallX')],[P('GET /health','BodyX'),P('healthy; model_loaded = true','BodyX'),P('The backend starts and the configured model is available.','BodyX')],[P('POST /predict smoke test','BodyX'),P('Drowsy; confidence about 0.91; severity 2','BodyX'),P('Image decode, inference, and response formatting work end to end.','BodyX')],[P('Model inspection','BodyX'),P('Alert, Drowsy, Low_Vigilant, Non_Drowsy','BodyX'),P('The active checkpoint is a drowsiness classifier.','BodyX')],[P('Frontend lint','BodyX'),P('Passed','BodyX'),P('No ESLint warnings or errors were reported.','BodyX')],[P('Frontend build','BodyX'),P('Passed','BodyX'),P('Next.js production compilation succeeds.','BodyX')],[P('Alarm threshold','BodyX'),P('Five seconds of continuous Drowsy status','BodyX'),P('Temporal logic is present and requires live consecutive results.','BodyX')]], [42*mm,55*mm,67*mm],7.7))
S += [P('6.1 Task 6 validation matrix','H2X')]
S.append(T([[P('Feature','SmallX'),P('Validation procedure','SmallX'),P('Expected evidence','SmallX')],[P('HOG','BodyX'),P('Run a valid frame through the feature function.','BodyX'),P('Non-zero descriptor length and summary statistics.','BodyX')],[P('Sobel / morphology','BodyX'),P('Run gradient magnitude, Otsu threshold, opening, and closing.','BodyX'),P('Edge density and morphology flag in metadata.','BodyX')],[P('Optical flow','BodyX'),P('Send moving consecutive frames and identical consecutive frames.','BodyX'),P('Movement produces a higher magnitude than identical frames.','BodyX')],[P('Alarm','BodyX'),P('Run continuous live monitoring with Drowsy outputs for at least five seconds.','BodyX'),P('Audio/tone and visual alarm appear after the threshold.','BodyX')],[P('Reset','BodyX'),P('Stop monitoring or send a non-drowsy result.','BodyX'),P('Alarm, streak, and previous-frame state reset.','BodyX')]], [35*mm,82*mm,47*mm],7.6))
S.append(P('The feature values used in a final demonstration must be recorded from the running implementation. Example values in the code appendix are response-format examples, not measured results from the untouched repository.','CallX'))
# 7
S.append(PageBreak()); S += [P('7. Limitations, Safety, and Reliability','H1X'),P('The Task 6 components improve the breadth of the computer-vision pipeline, but they do not eliminate the limitations identified in the earlier reports. A careful report must distinguish a working prototype from a validated driver-safety product.')]
S.append(T([[P('Limitation','SmallX'),P('Why it matters','SmallX'),P('Required follow-up','SmallX')],[P('Frame-level classifier','BodyX'),P('A single prediction can be unstable and does not directly measure duration of eye closure.','BodyX'),P('Use temporal smoothing and add facial landmarks or a dedicated eye-state detector.','BodyX')],[P('HOG sensitivity','BodyX'),P('Lighting, glasses, pose, and image quality change gradient distributions.','BodyX'),P('Test across subjects, lighting, glasses, and camera positions.','BodyX')],[P('Optical-flow ambiguity','BodyX'),P('Motion can come from the head, camera, background, or compression rather than drowsiness.','BodyX'),P('Use a face/eye ROI, reset state correctly, and report flow as supporting evidence.','BodyX')],[P('Audio permissions','BodyX'),P('Browsers may block audio until the user interacts with the page.','BodyX'),P('Prime audio on Start Monitoring and test alarm.mp3 in the target browser.','BodyX')],[P('Dataset generalization','BodyX'),P('Random frame splits can overestimate performance when frames share subjects or videos.','BodyX'),P('Use subject/video-level held-out evaluation.','BodyX')]], [39*mm,69*mm,56*mm],7.5))
S += [P('7.1 What counts as a successful Task 6 demonstration','H2X'),P('The team should show the working frontend, a backend response containing the CV metadata, a consecutive-frame optical-flow comparison, and the five-second alarm behavior. The demonstration should also state that HOG, optical flow, Sobel, thresholding, and morphology are documented here but were not applied to the repository source because the submission instruction required the codebase to remain untouched.')]
S.append(P('The alarm should be described as a warning aid. It should never encourage a driver to continue driving while drowsy; the safe action is to stop and rest.','CallX'))
# 8
S.append(PageBreak()); S += [P('8. Remaining 25% of the Project','H1X'),P('The final 25% is the validation and reliability phase. It should convert the integrated prototype into a defensible final project by measuring performance, validating real-world conditions, and completing the deployment and documentation work.')]
S.append(T([[P('Priority','SmallX'),P('Remaining work','SmallX'),P('Completion evidence','SmallX')],[P('High','BodyX'),P('Formal model evaluation on a subject/video-level held-out set: accuracy, precision, recall, F1, confusion matrix, and per-class results.','BodyX'),P('Reproducible evaluation script and metric tables.','BodyX')],[P('High','BodyX'),P('Direct eye-closure measurement using facial landmarks or a dedicated eye-state model; measure continuous closure duration.','BodyX'),P('Eye-region evidence tied to the alarm decision.','BodyX')],[P('High','BodyX'),P('Temporal robustness: smoothing, missing-frame handling, configurable thresholds, false-alarm and missed-alarm analysis.','BodyX'),P('Scenario matrix across people and conditions.','BodyX')],[P('Medium','BodyX'),P('Production validation: environment variables, CORS, model availability, cold starts, timeout, and frontend-backend connectivity.','BodyX'),P('Production smoke test and deployment checklist.','BodyX')],[P('Medium','BodyX'),P('Alarm and safety UX: alarm.mp3 testing, audio permission handling, mute/reset control, visible countdown, and safety messaging.','BodyX'),P('Final live demo and user instructions.','BodyX')],[P('Low','BodyX'),P('Final documentation, session export, experiment tracking, model provenance, and reproducibility notes.','BodyX'),P('Final README and submission package.','BodyX')]], [21*mm,101*mm,42*mm],7.4))
S += [P('Recommended order','H2X'),P('First complete the held-out evaluation and direct eye-closure measurement. Then tune temporal behavior and validate the deployment environment. Finally polish the alarm experience and documentation. HOG and optical flow strengthen the computer-vision coursework component, but they should not be presented as proof of eye closure by themselves.')]
# 9
S.append(PageBreak()); S += [P('9. Conclusion','H1X'),P('Project Task 6 continues the Driver Drowsiness Detection System from the functioning Task 5 web prototype toward a broader and more interpretable computer-vision pipeline. The existing camera capture, validation, YOLO inference, frontend feedback, session statistics, and five-second warning mechanism remain the system foundation.'),P('The Task 6 design contributes three connected CV components: HOG for local gradient structure, optical flow for frame-to-frame motion, and Sobel thresholding with morphology for edge and binary-region analysis. The response design exposes these measurements so they can be inspected and evaluated rather than discarded.')]
S.append(P('The source codebase was not changed. The required module and integration snippets are included in this report as a controlled implementation plan. The final 25% is the work needed to implement and validate the feature branch, measure generalization, add direct eye-state evidence, verify deployment, and finalize safety-oriented documentation.','CallX'))
S += [P('Code and project files referenced','H2X'),P('backend/app/services/image_processing.py · backend/app/services/inference.py · backend/app/routes/predict.py · backend/app/models/model.py · frontend/app/page.jsx · frontend/components/Camera.jsx · ml_pipeline/train.py · backend/weights/best.pt','SmallX'),P('Submission note','H2X'),P('This report is prepared as a continuation of the earlier Task 5 report and follows the Project Task 6 requirements: project title, team number, all team members, approximately 75% milestone, integrated-system discussion, current evidence, and remaining 25%.','SmallX')]
doc.build(S)
print(OUT)
