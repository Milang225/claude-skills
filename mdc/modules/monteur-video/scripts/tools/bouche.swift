// Ouverture de la bouche et sourire (Apple Vision, repères du visage) : une ligne CSV par image.
// Usage : swift bouche.swift <dossier_images>   → fichier,ouverture,sourire  (ouverture = hauteur intérieure des lèvres / hauteur du visage)
import Foundation
import Vision
import AppKit
let dir = CommandLine.arguments[1]
let files = try FileManager.default.contentsOfDirectory(atPath: dir).filter { $0.hasSuffix(".jpg") }.sorted()
print("fichier,ouverture,sourire")
for f in files {
    guard let img = NSImage(contentsOfFile: dir + "/" + f), let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
    let req = VNDetectFaceLandmarksRequest()
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    guard let face = req.results?.first, let lm = face.landmarks, let inner = lm.innerLips, let outer = lm.outerLips else { print("\(f),,"); continue }
    let ip = inner.normalizedPoints, op = outer.normalizedPoints
    let open = (ip.map { $0.y }.max()! - ip.map { $0.y }.min()!)
    // sourire : coins de la bouche plus hauts que le centre de la lèvre inférieure
    let left = op.min(by: { $0.x < $1.x })!, right = op.max(by: { $0.x < $1.x })!
    let low = op.map { $0.y }.min()!
    let smile = ((left.y + right.y) / 2 - low)
    print("\(f),\(open),\(smile)")
}
