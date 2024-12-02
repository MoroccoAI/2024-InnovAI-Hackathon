import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

class HuggingFaceService {
  final String apiKey = "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"; // Hugging Face API key
  final String xrayModelId = "lxyuan/vit-xray-pneumonia-classification"; // X-Ray model ID
  final String mixtralModelId = "mistralai/Mixtral-8x7B-Instruct-v0.1"; // Text generation model ID
  final String translationModelId = "atlasia/Terjman-Ultra"; // English-to-Darija translation model ID

  /// Analyze an X-ray image using the Hugging Face Inference API
  Future<List<dynamic>> analyzeXRay(File imageFile) async {
    final url = Uri.parse("https://api-inference.huggingface.co/models/$xrayModelId");
    final headers = {
      "Authorization": "Bearer $apiKey",
      "Content-Type": "application/octet-stream",
    };

    try {
      print("Analyzing X-Ray with model: $xrayModelId");

      final imageBytes = await imageFile.readAsBytes();

      final response = await http.post(
        url,
        headers: headers,
        body: imageBytes,
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as List<dynamic>;
        print("X-Ray Analysis Response: $data");
        return data;
      } else {
        throw Exception("X-Ray model error: ${response.reasonPhrase}");
      }
    } catch (e) {
      throw Exception("Failed to analyze X-ray: $e");
    }
  }

  /// Generate a description using the Mixtral model based on the X-ray analysis percentage
  Future<String> generateDescriptionUsingModel(List<dynamic> predictions) async {
    if (predictions.isEmpty) {
      return "No significant results were found. Please try again with a different X-Ray image.";
    }

    final prediction = predictions[0];
    final label = prediction['label'];
    final score = (prediction['score'] * 100).toDouble();

    final url = Uri.parse("https://api-inference.huggingface.co/models/$mixtralModelId");
    final headers = {
      "Authorization": "Bearer $apiKey",
      "Content-Type": "application/json",
    };

    final prompt = label.toLowerCase() == "pneumonia"
        ? "The X-ray analysis indicates a $score% likelihood of pneumonia. Provide a detailed explanation of this finding, describe what pneumonia is, and recommend whether the patient should consult a doctor based on this likelihood."
        : "The X-ray analysis indicates a $score% likelihood of $label. Provide a detailed explanation of this finding, describe what this condition is, and recommend whether the patient should consult a doctor based on this likelihood.";

    final body = jsonEncode({
      "inputs": prompt,
      "parameters": {
        "temperature": 0.7,
        "max_new_tokens": 1024,
        "repetition_penalty": 1.1,
      },
    });

    try {
      print("Sending request to Mixtral model...");
      final response = await http.post(
        url,
        headers: headers,
        body: body,
      );

      print("Mixtral API Response Status: ${response.statusCode}");
      print("Mixtral API Response Body: ${response.body}");

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as List<dynamic>;
        if (data.isNotEmpty && data[0]["generated_text"] != null) {
          String generatedText = data[0]["generated_text"].trim();

          if (generatedText.contains(prompt)) {
            generatedText = generatedText.replaceFirst(prompt, "").trim();
          }

          return generatedText;
        } else {
          throw Exception("Unexpected response format from Mixtral model.");
        }
      } else {
        throw Exception("Mixtral model error: ${response.reasonPhrase}");
      }
    } catch (e) {
      return "Unable to generate a detailed description at this time.";
    }
  }

  /// Clean up translated text
  String cleanupTranslatedText(String text) {
    return text
        .replaceAll(RegExp(r'\s+'), ' ') // Remove extra spaces
        .replaceAll(RegExp(r'\.+'), '.') // Remove multiple periods
        .trim();
  }

  /// Translate text from English to Darija using the Terjman model
  Future<String> translateToDarija(String englishText) async {
    final url = Uri.parse("https://api-inference.huggingface.co/models/$translationModelId");
    final headers = {
      "Authorization": "Bearer $apiKey",
      "Content-Type": "application/json",
    };

    // Split text into chunks
    List<String> textChunks = [];
    int chunkSize = 500;

    for (var i = 0; i < englishText.length; i += chunkSize) {
      int end = (i + chunkSize < englishText.length) ? i + chunkSize : englishText.length;
      // Try to split at the last complete sentence
      while (end < englishText.length && !englishText[end].contains(RegExp(r'[.!?]'))) {
        end++;
      }
      textChunks.add(englishText.substring(i, end));
    }

    List<String> translatedChunks = [];

    for (String chunk in textChunks) {
      final body = jsonEncode({
        "inputs": chunk,
        "parameters": {
          "max_length": 512,
          "num_return_sequences": 1,
          "temperature": 0.7,
          "do_sample": true,
          "top_p": 0.95,
        },
        "options": {
          "wait_for_model": true,
        }
      });

      try {
        print("Translating chunk to Darija using Terjman model...");
        final response = await http.post(
          url,
          headers: headers,
          body: body,
        );

        print("Terjman Model Response Status: ${response.statusCode}");
        print("Terjman Model Response Body: ${response.body}");

        if (response.statusCode == 200) {
          final data = jsonDecode(response.body);

          if (data is List && data.isNotEmpty && data[0].containsKey("generated_text")) {
            final translatedTextRaw = data[0]["generated_text"];
            final translatedText = utf8.decode(translatedTextRaw.runes.toList());
            translatedChunks.add(translatedText);
          } else {
            throw Exception("Unexpected response format from Terjman model: $data");
          }
        } else {
          // Add delay and retry logic for 503 errors
          if (response.statusCode == 503) {
            await Future.delayed(Duration(seconds: 20));
            // Retry the request
            continue;
          }
          throw Exception("Terjman model error: ${response.reasonPhrase}");
        }

        // Add a small delay between chunks to avoid rate limiting
        await Future.delayed(Duration(milliseconds: 500));

      } catch (e) {
        print("Error during translation: $e");
        translatedChunks.add("Error translating this portion.");
      }
    }

    // Combine and clean up all translated chunks
    return cleanupTranslatedText(translatedChunks.join(" "));
  }

  /// Retry mechanism for API calls
  Future<http.Response> retryRequest(Future<http.Response> Function() request,
      {int maxAttempts = 3, int delaySeconds = 20}) async {
    int attempts = 0;
    while (attempts < maxAttempts) {
      try {
        final response = await request();
        if (response.statusCode != 503) {
          return response;
        }
        attempts++;
        if (attempts < maxAttempts) {
          await Future.delayed(Duration(seconds: delaySeconds));
        }
      } catch (e) {
        attempts++;
        if (attempts >= maxAttempts) rethrow;
        await Future.delayed(Duration(seconds: delaySeconds));
      }
    }
    throw Exception("Max retry attempts reached");
  }
}