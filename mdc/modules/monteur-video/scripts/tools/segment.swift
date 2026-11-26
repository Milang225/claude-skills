// Détourage de la personne (Apple Vision) : écrit un masque PNG en niveaux de gris par image.
// Usage : swift segment.swift <dossier_images_entree> <dossier_masques_sortie>
import Foundation
import Vision
import AppKit
import CoreImage

let inDir = CommandLine.arguments[1], outDir = CommandLine.arguments[2]
try? FileManager.default.createDirectory(atPath: outDir, withIntermediateDirectories: true)
let files = try FileManager.default.contentsOfDirectory(atPath: inDir).filter { $0.hasSuffix(".jpg") || $0.hasSuffix(".png") }.sorted()
let ctx = CIContext()
for f in files {
    guard let img = NSImage(contentsOfFile: inDir + "/" + f),
          let cg = img.cgImage(forProposedRect: nil, context: nil, hints: nil) else { continue }
    let req = VNGeneratePersonSegmentationRequest()
    req.qualityLevel = .accurate
    req.outputPixelFormat = kCVPixelFormatType_OneComponent8
    try? VNImageRequestHandler(cgImage: cg, options: [:]).perform([req])
    guard let buf = req.results?.first?.pixelBuffer else { continue }
    var mask = CIImage(cvPixelBuffer: buf)
    let sx = CGFloat(cg.width) / mask.extent.width, sy = CGFloat(cg.height) / mask.extent.height
    mask = mask.transformed(by: CGAffineTransform(scaleX: sx, y: sy))
    let name = (f as NSString).deletingPathExtension + ".png"
    let url = URL(fileURLWithPath: outDir + "/" + name)
    try? ctx.writePNGRepresentation(of: mask, to: url, format: .L8, colorSpace: CGColorSpaceCreateDeviceGray())
}
