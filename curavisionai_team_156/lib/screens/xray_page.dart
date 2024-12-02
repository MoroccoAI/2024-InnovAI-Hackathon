import 'dart:io';
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:image_picker/image_picker.dart';
import 'services/hugging_face_service.dart';

class XRayPage extends StatefulWidget {
  const XRayPage({super.key});

  @override
  State<XRayPage> createState() => _XRayPageState();
}

class _XRayPageState extends State<XRayPage> {
  File? _image; // Selected image file
  String? _englishResult; // Analysis result in English
  String? _darijaResult; // Translated result in Darija
  bool _isLoading = false; // Loading state for initial analysis
  bool _isTranslating = false; // Loading state for Darija translation

  final ImagePicker _picker = ImagePicker(); // Instance of ImagePicker
  final HuggingFaceService huggingFaceService = HuggingFaceService(); // Instance of HuggingFaceService

  /// Pick an image from the gallery
  Future<void> _pickImage() async {
    final pickedFile = await _picker.pickImage(source: ImageSource.gallery);
    if (pickedFile != null) {
      setState(() {
        _image = File(pickedFile.path); // Store the selected image
        _englishResult = null; // Reset previous English result
        _darijaResult = null; // Reset previous Darija result
        _isLoading = false; // Reset loading states
        _isTranslating = false;
      });
      _analyzeImage(); // Automatically analyze the image after selection
    }
  }

  /// Analyze the selected X-ray image
  Future<void> _analyzeImage() async {
    if (_image == null) return;

    setState(() {
      _isLoading = true; // Show loading spinner for initial analysis
      _englishResult = null; // Clear previous English result
      _darijaResult = null; // Clear previous Darija result
    });

    try {
      // Step 1: Call Hugging Face API for X-ray analysis
      final analysisResult = await huggingFaceService.analyzeXRay(_image!);

      // Step 2: Generate the description using the Mixtral model
      print("Calling Mixtral model for detailed explanation...");
      final englishDescription = await huggingFaceService.generateDescriptionUsingModel(analysisResult);

      // Immediately show the English result
      setState(() {
        _englishResult = englishDescription; // Display the English result
        _isLoading = false; // Stop loading spinner for English result
        _isTranslating = true; // Start spinner for Darija translation
      });

      // Step 3: Translate the English description to Darija
      print("Translating the result to Darija...");
      final darijaTranslation = await huggingFaceService.translateToDarija(englishDescription);

      setState(() {
        _darijaResult = darijaTranslation; // Display the Darija translation
        _isTranslating = false; // Stop spinner for Darija translation
      });
    } catch (e) {
      setState(() {
        _englishResult = "Error: $e"; // Show error message
        _darijaResult = null; // Clear the Darija result in case of error
        _isLoading = false; // Stop all spinners
        _isTranslating = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        iconTheme: const IconThemeData(
          color: Colors.white, // Back button color (white)
        ),
        title: Text(
          'X-Ray Analysis',
          style: GoogleFonts.montserrat(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.white, // Title color
          ),
        ),
        centerTitle: true,
        backgroundColor: Colors.blue[700], // Lighter blue for X-Ray Page
      ),
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Expanded(
            child: SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // Header Section
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: Colors.blue[100], // Decorative light blue background
                      borderRadius: const BorderRadius.only(
                        bottomLeft: Radius.circular(40),
                        bottomRight: Radius.circular(40),
                      ),
                    ),
                    child: Column(
                      children: [
                        Icon(
                          Icons.radio,
                          size: 80,
                          color: Colors.blue[700], // X-Ray icon
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Welcome to X-Ray Analysis',
                          style: GoogleFonts.montserrat(
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                            color: Colors.blue[700],
                          ),
                          textAlign: TextAlign.center,
                        ),
                        const SizedBox(height: 7),
                        Text(
                          'Upload your X-Rays for AI-powered diagnostics.',
                          style: GoogleFonts.lato(
                            fontSize: 16,
                            color: Colors.grey[700],
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 16),

                  // Upload Button
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 24.0),
                    child: ElevatedButton.icon(
                      onPressed: _pickImage, // Trigger the image picker
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.blue[700],
                        padding: const EdgeInsets.symmetric(vertical: 20, horizontal: 16), // Added padding
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12), // Rounded corners
                        ),
                      ),
                      icon: const Icon(Icons.upload_rounded, color: Colors.white),
                      label: Text(
                        'Upload X-Ray',
                        style: GoogleFonts.montserrat(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                          color: Colors.white,
                        ),
                      ),
                    ),
                  ),

                  const SizedBox(height: 16),

                  // Display Selected Image
                  if (_image != null)
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 24.0),
                      child: ClipRRect(
                        borderRadius: BorderRadius.circular(12), // Rounded corners
                        child: Image.file(
                          _image!,
                          height: 300,
                          fit: BoxFit.cover, // Scale image to fit
                        ),
                      ),
                    ),

                  // Loading Spinner or Results Section
                  if (_isLoading) ...[
                    const SizedBox(height: 16),
                    const Center(child: CircularProgressIndicator()), // Show spinner while analyzing
                  ] else if (_englishResult != null) ...[
                    const SizedBox(height: 16),
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 24),
                      child: Container(
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: Colors.grey[100], // Background for result box
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: Colors.blue[300]!), // Border for the result container
                        ),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            // English Result
                            Text(
                              "Analysis Result (English):\n\n$_englishResult",
                              style: GoogleFonts.lato(
                                fontSize: 16,
                                fontWeight: FontWeight.w600,
                                color: Colors.blue[700],
                              ),
                              textAlign: TextAlign.center,
                            ),
                            const SizedBox(height: 16),
                            // Darija Result
                            Column(
                              children: [
                                Text(
                                  "Analysis Result (Darija):",
                                  style: GoogleFonts.lato(
                                    fontSize: 16,
                                    fontWeight: FontWeight.w600,
                                    color: Colors.blue[700],
                                  ),
                                  textAlign: TextAlign.center,
                                ),
                                const SizedBox(height: 8),
                                if (_isTranslating)
                                  const Center(child: CircularProgressIndicator()), // Show spinner for Darija translation
                                if (_darijaResult != null)
                                  Text(
                                    _darijaResult!,
                                    style: GoogleFonts.lato(
                                      fontSize: 16,
                                      fontWeight: FontWeight.w600,
                                      color: Colors.blue[700],
                                    ),
                                    textAlign: TextAlign.center,
                                  ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],

                  const SizedBox(height: 16),
                ],
              ),
            ),
          ),

          // Footer Section
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Text(
              'CuraVision AI - Empowering Your Health',
              style: GoogleFonts.lato(
                fontSize: 14,
                fontWeight: FontWeight.w400,
                color: Colors.grey[600],
              ),
              textAlign: TextAlign.center,
            ),
          ),
        ],
      ),
    );
  }
}