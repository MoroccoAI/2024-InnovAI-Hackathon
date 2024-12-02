import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

class CameraPage extends StatefulWidget {
  final List<CameraDescription> cameras;

  const CameraPage({Key? key, required this.cameras}) : super(key: key);

  @override
  _CameraPageState createState() => _CameraPageState();
}

class _CameraPageState extends State<CameraPage> {
  late CameraController _controller;
  XFile? _pictureFile;

  @override
  void initState() {
    super.initState();
    // Initialiser le contrôleur de caméra avec la première caméra disponible
    _controller = CameraController(
      widget.cameras[0],
      ResolutionPreset.max,
    );

    // Initialiser le contrôleur
    _controller.initialize().then((_) {
      if (!mounted) return;
      setState(() {});
    }).catchError((Object e) {
      if (e is CameraException) {
        switch (e.code) {
          case 'CameraAccessDenied':
            print('Accès à la caméra refusé');
            break;
          default:
            print('Erreur de caméra : ${e.description}');
            break;
        }
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Capture d\'image'),
      ),
      body: Column(
        children: [
          // Prévisualisation de la caméra
          Expanded(
            child: _controller.value.isInitialized
                ? CameraPreview(_controller)
                : const Center(child: CircularProgressIndicator()),
          ),
          Padding(
            padding: const EdgeInsets.all(20.0),
            child: ElevatedButton(
              onPressed: () async {
                try {
                  final image = await _controller.takePicture();
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => ImageConfirmationPage(imagePath: image.path),
                    ),
                  );
                } catch (e) {
                  print('Erreur lors de la capture : $e');
                }
              },
              child: const Text('Capturer'),
            ),
          ),
        ],
      ),
    );
  }
}

class ImageConfirmationPage extends StatelessWidget {
  final String imagePath;

  const ImageConfirmationPage({Key? key, required this.imagePath}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Confirmer l\'image'),
      ),
      body: Column(
        children: [
          Expanded(
            child: Image.file(
              File(imagePath),
              fit: BoxFit.contain,
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(20.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: () {
                    Navigator.pop(context);
                    Navigator.pop(context, imagePath);
                  },
                  child: const Text('Utiliser'),
                ),
                ElevatedButton(
                  onPressed: () {
                    Navigator.pop(context);
                  },
                  child: const Text('Reprendre'),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
