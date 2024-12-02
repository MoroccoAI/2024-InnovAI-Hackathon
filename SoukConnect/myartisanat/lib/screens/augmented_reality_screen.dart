import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'package:image_picker/image_picker.dart';
import 'package:permission_handler/permission_handler.dart';
import 'camera_page.dart'; // Importez le fichier de la caméra

class AugmentedRealityScreen extends StatefulWidget {
  const AugmentedRealityScreen({Key? key}) : super(key: key);

  @override
  _AugmentedRealityScreenState createState() => _AugmentedRealityScreenState();
}

class _AugmentedRealityScreenState extends State<AugmentedRealityScreen> {
  final ImagePicker _picker = ImagePicker();

  // Méthode pour importer une image depuis la galerie
  Future<void> _pickImageFromGallery() async {
    var status = await Permission.photos.request(); // Demande de permission pour la galerie
    if (status.isGranted) {
      try {
        final XFile? image = await _picker.pickImage(source: ImageSource.gallery);
        if (image != null) {
          // Naviguer vers la page de confirmation avec l'image sélectionnée
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => ImageConfirmationPage(imagePath: image.path),
            ),
          );
        }
      } catch (e) {
        print('Erreur lors de la sélection de l\'image : $e');
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Erreur : ${e.toString()}')),
        );
      }
    } else {
      // Afficher un message si la permission est refusée
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Permission galerie refusée')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Réalité Augmentée"),
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(
              Icons.camera_alt_outlined,
              size: 100,
              color: Colors.black,
            ),
            const SizedBox(height: 20),
            const Text(
              'Réalité Augmentée',
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: Colors.black,
              ),
            ),
            const SizedBox(height: 10),
            const Text(
              'Scannez un produit artisanal pour découvrir son histoire',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 16,
                color: Colors.black87,
              ),
            ),
            const SizedBox(height: 40),
            ElevatedButton(
              onPressed: () async {
                var cameraStatus = await Permission.camera.request();
                if (cameraStatus.isGranted) {
                  final cameras = await availableCameras();
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (context) => CameraPage(cameras: cameras),
                    ),
                  );
                } else {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(content: Text('Permission caméra requise')),
                  );
                }
              },
              child: const Text("Scanner avec Caméra"),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _pickImageFromGallery, // Appel de la méthode fusionnée
              child: const Text("Importer depuis Galerie"),
            ),
          ],
        ),
      ),
    );
  }
}
