import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class ViewReportsPage extends StatelessWidget {
  const ViewReportsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        iconTheme: const IconThemeData(
          color: Colors.white, // Back button color
        ),
        title: Text(
          'Previous Reports',
          style: GoogleFonts.montserrat(
            fontSize: 24,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
        centerTitle: true,
        backgroundColor: Colors.blue[500], // Different color for this page
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemCount: 10, // Placeholder for the number of reports
        itemBuilder: (context, index) {
          return Card(
            margin: const EdgeInsets.symmetric(vertical: 8.0),
            child: ListTile(
              leading: const Icon(Icons.description, color: Colors.blue),
              title: Text(
                'Report ${index + 1}',
                style: GoogleFonts.montserrat(fontWeight: FontWeight.bold),
              ),
              subtitle: Text(
                'Date: ${DateTime.now().toLocal()}',
                style: GoogleFonts.lato(),
              ),
              onTap: () {
                // TODO: Add functionality to view detailed report
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Report ${index + 1} clicked')),
                );
              },
            ),
          );
        },
      ),
    );
  }
}