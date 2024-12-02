import 'package:flutter/material.dart';

class ProductDetailPage extends StatelessWidget {
  final String title;
  final String author;
  final String region;
  final String imagePath;

  const ProductDetailPage({
    super.key,
    required this.title,
    required this.author,
    required this.region,
    required this.imagePath,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(title),
        backgroundColor: Colors.blueAccent,
      ),
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Image principale
            Image.asset(
              imagePath,
              width: double.infinity,
              height: 250,
              fit: BoxFit.cover,
            ),
            SizedBox(height: 16),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                  Text(
                    'Par $author • $region',
                    style: TextStyle(fontSize: 16, color: Colors.grey),
                  ),
                  SizedBox(height: 20),
                  // Boutons d'informations
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _infoButton(Icons.info, 'Informations'),
                      _infoButton(Icons.history, 'Histoire'),
                      _infoButton(Icons.settings, 'Processus'), // Icône correcte
                      _infoButton(Icons.translate, 'Traduction'),
                    ],
                  ),
                  SizedBox(height: 20),
                  // Techniques et symboles
                  _sectionTitle('Techniques'),
                  Text(
                    'Double nœud • Laine naturelle • Teintures végétales',
                    style: TextStyle(fontSize: 16),
                  ),
                  SizedBox(height: 20),
                  _sectionTitle('Symboles'),
                  Text(
                    'Losange - Protection\nTriangle - Féminité',
                    style: TextStyle(fontSize: 16),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  // Widget pour créer un bouton d'information
  Widget _infoButton(IconData icon, String label) {
    return Column(
      children: [
        Icon(icon, size: 32, color: Colors.blueAccent),
        SizedBox(height: 8),
        Text(label),
      ],
    );
  }

  // Widget pour les titres de section
  Widget _sectionTitle(String title) {
    return Text(
      title,
      style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
    );
  }
}
