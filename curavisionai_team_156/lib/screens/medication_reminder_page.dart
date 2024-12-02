import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class MedicationReminderPage extends StatelessWidget {
  const MedicationReminderPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        iconTheme: const IconThemeData(
          color: Colors.white, // Back button color (white)
        ),
        title: Text(
          'Medication Reminder',
          style: GoogleFonts.montserrat(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.white, // Title color
          ),
        ),
        centerTitle: true,
        backgroundColor: Colors.purple[800], // Purple theme for Medication Reminder
      ),
      body: Column(
        children: [
          Expanded(
            child: Center(
              child: Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center, // Center content vertically
                  crossAxisAlignment: CrossAxisAlignment.center, // Center content horizontally
                  children: [
                    // Icon representing the feature
                    Icon(
                      Icons.alarm, // Alarm icon
                      size: 100,
                      color: Colors.purple[800],
                    ),
                    const SizedBox(height: 24), // Spacing between icon and text
                    // "Coming Soon" Title
                    Text(
                      'Coming Soon!',
                      style: GoogleFonts.lato(
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                        color: Colors.purple[800],
                      ),
                    ),
                    const SizedBox(height: 16), // Spacing between title and description
                    // Description Text
                    Text(
                      'The Medication Reminder feature is under development. '
                          'Soon, you’ll be able to set reminders to stay on top of your medication schedule.',
                      textAlign: TextAlign.center,
                      style: GoogleFonts.lato(
                        fontSize: 16,
                        color: Colors.grey[700],
                      ),
                    ),
                    const SizedBox(height: 32), // Spacing before the action button
                    // Back to Home Button
                    ElevatedButton(
                      onPressed: () {
                        Navigator.pop(context); // Navigate back to the previous page
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.purple[800], // Button color
                        padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8), // Rounded corners
                        ),
                      ),
                      child: Text(
                        'Back to Home',
                        style: GoogleFonts.lato(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                          color: Colors.white, // Text color
                        ),
                      ),
                    ),
                  ],
                ),
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