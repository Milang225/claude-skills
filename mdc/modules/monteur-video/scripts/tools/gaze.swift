// Détection du regard (Apple Vision) : orientation de la tête + position des pupilles, image par image.
// Usage : swift gaze.swift <dossier_images> > sortie.csv   (images nommées  t_<secondes>.jpg)
import Foundation
import Vision
import AppKit

func center(_ pts: [CGPoint]) -> CGPoint {
    let xs = pts.map { $0.x }, ys = pts.map { $0.y }
    return CGPoint(x: (xs.min()! + xs.max()!) / 2, y: (ys.min()! + ys.max()!) / 2)
}
func span(_ pts: [CGPoint]) -> CGSize {
    let xs = pts.map { $0.x }, ys = pts.map { $0.y }
    return CGSize(width: xs.max()! - xs.min()!, height: ys.max()! - ys.min()!)
}

let dir = CommandLine.arguments[1]
let files = try FileManager.default.contentsOfDirectory(atPath: dir).filter { $0.hasSuffix(".jpg") }.sorted()
print("t,face,yaw,pitch,roll,px,py,eyeopen")
for f in files {
    let t = f.replacingOccurrences(of: "t_", with: "").replacingOccurrences(of: ".jpg", with: "")
    guard let img = NSImage(contentsOfFile: dir + "/" + f),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
    let req = VNDetectFaceLandmarksRequest()
    let pose = VNDetectFaceRectanglesRequest()
    pose.revision = VNDetectFaceRectanglesRequestRevision3
    let h = VNImageRequestHandler(cgImage: cg, options: [:])
    try? h.perform([req, pose])
    guard let face = (req.results ?? []).max(by: { $0.boundingBox.width < $1.boundingBox.width }) else {
        print("\(t),0,,,,,,"); continue
    }
    let pf = (pose.results ?? []).max(by: { $0.boundingBox.width < $1.boundingBox.width })
    let yaw = pf?.yaw?.doubleValue ?? .nan, pitch = pf?.pitch?.doubleValue ?? .nan, roll = pf?.roll?.doubleValue ?? .nan
    var px = Double.nan, py = Double.nan, open = Double.nan
    if let lm = face.landmarks, let le = lm.leftEye?.normalizedPoints, let re = lm.rightEye?.normalizedPoints,
       let lp = lm.leftPupil?.normalizedPoints.first, let rp = lm.rightPupil?.normalizedPoints.first, le.count > 2, re.count > 2 {
        let lc = center(le), rc = center(re), ls = span(le), rs = span(re)
        px = Double(((lp.x - lc.x) / max(ls.width, 1e-3) + (rp.x - rc.x) / max(rs.width, 1e-3)) / 2)
        py = Double(((lp.y - lc.y) / max(ls.height, 1e-3) + (rp.y - rc.y) / max(rs.height, 1e-3)) / 2)
        open = Double((ls.height / max(ls.width, 1e-3) + rs.height / max(rs.width, 1e-3)) / 2)
    }
    print("\(t),1,\(yaw),\(pitch),\(roll),\(px),\(py),\(open)")
}
