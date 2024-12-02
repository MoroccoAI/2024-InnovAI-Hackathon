import 'package:flutter/material.dart';
import 'screens/augmented_reality_screen.dart'; // Assurez-vous d'importer la page AR
import 'screens/product_detail_page.dart'; // Importez la page de détails

void main() {
  runApp(const ArtisanatApp());
}

class ArtisanatApp extends StatelessWidget {
  const ArtisanatApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _currentIndex = 0;

  final List<Map<String, String>> categories = [
    {'title': 'Le plâtre et le zellige', 'image': 'assets/images/zelig.jpg'},
    {'title': 'Tapis', 'image': 'assets/images/tapis.jpg'},
    {'title': 'Bijoux', 'image': 'assets/images/bijoux.jpg'},
    {'title': 'Bois sculpté', 'image': 'assets/images/bois.jpg'},
    {'title': 'Les habits traditionnels', 'image': 'assets/images/habits_traditionnels.jpg'},
    {'title': 'La céramique et la poterie', 'image': 'assets/images/ceramique.jpg'},
    {'title': 'Le fer forgé', 'image': 'assets/images/fer_forge.jpg'},
    {'title': 'La Marqueterie et le Thuya', 'image': 'assets/images/marquetrie.jpg'},
    {'title': 'La dinanderie', 'image': 'assets/images/dinanderie.jpg'},
  ];

  final List<Map<String, String>> recommendedProducts = [
    {
      'title': 'Tapis Berbère',
      'price': '250 MAD',
      'image': 'assets/images/tapis_berbere.jpg',
    },
    {
      'title': 'Poterie de Fès',
      'price': '100 MAD',
      'image': 'assets/images/poterie_fes.jpg',
    },
  ];

  void _previousImage() {
    setState(() {
      _currentIndex = (_currentIndex - 1 + categories.length) % categories.length;
    });
  }

  void _nextImage() {
    setState(() {
      _currentIndex = (_currentIndex + 1) % categories.length;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: PreferredSize(
        preferredSize: Size.fromHeight(kToolbarHeight),
        child: Stack(
          children: [
            Positioned.fill(
              child: Image.asset(
                'assets/images/background.jpg',
                fit: BoxFit.cover,
              ),
            ),
            AppBar(
              backgroundColor: Colors.transparent,
              elevation: 0,
              title: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Image.asset(
                    'assets/images/flag.png',
                    height: 50,
                  ),
                  SizedBox(width: 10),
                  Text(
                    'SoukConnect',
                    style: TextStyle(
                      color: Color(0xFF095926),
                      fontWeight: FontWeight.w900,
                      fontSize: 40,
                      fontFamily: 'LastChristmas',
                      shadows: [
                        Shadow(
                          offset: Offset(2.0, 2.0),
                          blurRadius: 4.0,
                          color: Colors.black.withOpacity(0.5),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
              centerTitle: true,
              actions: [
                IconButton(
                  icon: Icon(
                    Icons.info_outline,
                    color: Colors.white,
                  ),
                  onPressed: () {
                    // Action à définir
                  },
                ),
              ],
            ),
          ],
        ),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Image principale avec navigation
              Container(
                width: double.infinity,
                height: 250,
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(16.0),
                  image: DecorationImage(
                    image: AssetImage(categories[_currentIndex]['image']!),
                    fit: BoxFit.cover,
                  ),
                ),
                child: Stack(
                  children: [
                    Positioned(
                      bottom: 10,
                      left: 10,
                      child: Container(
                        padding: EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                        decoration: BoxDecoration(
                          color: Colors.black54,
                          borderRadius: BorderRadius.circular(10),
                        ),
                        child: Text(
                          categories[_currentIndex]['title']!,
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                    ),
                    Positioned(
                      left: 0,
                      top: 0,
                      bottom: 0,
                      child: IconButton(
                        icon: Icon(Icons.arrow_back, color: Colors.white),
                        onPressed: _previousImage,
                      ),
                    ),
                    Positioned(
                      right: 0,
                      top: 0,
                      bottom: 0,
                      child: IconButton(
                        icon: Icon(Icons.arrow_forward, color: Colors.white),
                        onPressed: _nextImage,
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(height: 16),
              TextField(
                decoration: InputDecoration(
                  hintText: 'Rechercher des produits artisanaux',
                  prefixIcon: Icon(Icons.search),
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(8),
                  ),
                ),
              ),
              SizedBox(height: 16),
              Text(
                'Produits Recommandés',
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                ),
              ),
              SizedBox(height: 8),
              SingleChildScrollView(
                child: GridView.builder(
                  shrinkWrap: true, // Important pour que le GridView ne prenne que l'espace nécessaire
                  physics: NeverScrollableScrollPhysics(),
                  itemCount: recommendedProducts.length,
                  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                    crossAxisCount: 2,
                    crossAxisSpacing: 8,
                    mainAxisSpacing: 8,
                  ),
                  itemBuilder: (context, index) {
                    return GestureDetector(
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => ProductDetailPage(
                              title: recommendedProducts[index]['title']!,
                              author: 'Artisan inconnu',
                              region: 'Maroc',
                              imagePath: recommendedProducts[index]['image']!,
                            ),
                          ),
                        );
                      },
                      child: ProductCard(
                        title: recommendedProducts[index]['title']!,
                        price: recommendedProducts[index]['price']!,
                        imagePath: recommendedProducts[index]['image']!,
                      ),
                    );
                  },
                ),
              ),


              Center(
                child: ElevatedButton.icon(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => AugmentedRealityScreen(),
                      ),
                    );
                  },
                  icon: Icon(Icons.camera_alt),
                  label: Text('Activer Réalité Augmentée'),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blue,
                    foregroundColor: Colors.white,
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(20),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        items: [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Accueil',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.camera),
            label: 'AR',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.shopping_cart),
            label: 'Panier',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.book),
            label: 'Tutoriels',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.bar_chart),
            label: 'Stock',
          ),
        ],
      ),
    );
  }
}

// Définition du widget ProductCard
class ProductCard extends StatelessWidget {
  final String title;
  final String price;
  final String imagePath;

  const ProductCard({
    required this.title,
    required this.price,
    required this.imagePath,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 4.0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12.0),
      ),
      child: Column(
        children: [
          ClipRRect(
            borderRadius: BorderRadius.circular(12.0),
            child: Image.asset(
              imagePath,
              fit: BoxFit.cover,
              height: 120,
              width: double.infinity,
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                SizedBox(height: 4),
                Text(
                  price,
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.green,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
