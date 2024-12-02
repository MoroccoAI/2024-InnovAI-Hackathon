import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:curavisionai/screens/xray_page.dart';
import 'medication_page.dart';
import 'medication_reminder_page.dart';
import '../account_page.dart';

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'CuraVision AI',
          style: GoogleFonts.raleway(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        backgroundColor: Colors.blue[900], // Updated to a darker blue for Home Page
        centerTitle: false, // Align title to the left
        actions: [
          GestureDetector(
            onTap: () {
              // Navigate to the Account Page
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => const AccountPage(),
                ),
              );
            },
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16.0),
              child: Icon(
                Icons.account_circle,
                color: Colors.white, // White account icon
              ),
            ),
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: Center(
              child: Column(
                mainAxisSize: MainAxisSize.min, // Center widgets vertically
                children: [
                  // X-Ray Analysis Section
                  GestureDetector(
                    onTap: () {
                      // Navigate to the X-Ray Analysis Page
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => const XRayPage()),
                      );
                    },
                    child: Container(
                      margin:
                      const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
                      padding: const EdgeInsets.all(16.0),
                      width: double.infinity, // Make it take the full width
                      decoration: BoxDecoration(
                        color: Colors.blue[100], // Light blue background for this section
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.radio, // Icon for X-Ray Analysis
                            size: 48,
                            color: Colors.blue[800],
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'X-Ray Analysis',
                            style: GoogleFonts.lato(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                              color: Colors.blue[800],
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'AI-powered diagnostics for skeletal anomalies.',
                            textAlign: TextAlign.center,
                            style: GoogleFonts.lato(
                                fontSize: 14, color: Colors.grey[700]),
                          ),
                        ],
                      ),
                    ),
                  ),
                  // Medication Checker Section
                  GestureDetector(
                    onTap: () {
                      // Navigate to the Medication Checker Page
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (context) => const MedicationPage()),
                      );
                    },
                    child: Container(
                      margin:
                      const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
                      padding: const EdgeInsets.all(16.0),
                      width: double.infinity, // Make it take the full width
                      decoration: BoxDecoration(
                        color: Colors.green[100], // Light green background for this section
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.medication, // Icon for Medication Checker
                            size: 48,
                            color: Colors.green[800],
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Medication Checker',
                            style: GoogleFonts.lato(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                              color: Colors.green[800],
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Analyze medication interactions and find alternatives.',
                            textAlign: TextAlign.center,
                            style: GoogleFonts.lato(
                                fontSize: 14, color: Colors.grey[700]),
                          ),
                        ],
                      ),
                    ),
                  ),
                  // Medication Reminder Section
                  GestureDetector(
                    onTap: () {
                      // Navigate to the Medication Reminder Page
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => const MedicationReminderPage(),
                        ),
                      );
                    },
                    child: Container(
                      margin:
                      const EdgeInsets.symmetric(vertical: 8.0, horizontal: 16.0),
                      padding: const EdgeInsets.all(16.0),
                      width: double.infinity, // Make it take the full width
                      decoration: BoxDecoration(
                        color: Colors.purple[100], // Light purple background for this section
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.alarm, // Icon for Medication Reminder
                            size: 48,
                            color: Colors.purple[800],
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Medication Reminder',
                            style: GoogleFonts.lato(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                              color: Colors.purple[800],
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Set and manage reminders for your medications.',
                            textAlign: TextAlign.center,
                            style: GoogleFonts.lato(
                                fontSize: 14, color: Colors.grey[700]),
                          ),
                        ],
                      ),
                    ),
                  ),
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