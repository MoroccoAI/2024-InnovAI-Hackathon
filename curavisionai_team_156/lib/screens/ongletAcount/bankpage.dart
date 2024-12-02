// lib/pages/bank_cards_page.dart
import 'package:flutter/material.dart';

class BankCardsPage extends StatelessWidget {
  const BankCardsPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Bank & Cards'),
        backgroundColor: Color(0xFF2196F3),
        elevation: 0,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            buildCardItem(
              cardNumber: '**** **** **** 1234',
              cardType: 'Visa',
              expiryDate: '12/24',
            ),
            const SizedBox(height: 16),
            buildAddCardButton(),
          ],
        ),
      ),
    );
  }

  Widget buildCardItem({
    required String cardNumber,
    required String cardType,
    required String expiryDate,
  }) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFF2196F3), Color(0xFF64B5F6)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(15),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            cardNumber,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 22,
              letterSpacing: 2,
            ),
          ),
          const SizedBox(height: 20),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                cardType,
                style: const TextStyle(color: Colors.white),
              ),
              Text(
                'Expires: $expiryDate',
                style: const TextStyle(color: Colors.white),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget buildAddCardButton() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(15),
        border: Border.all(color: const Color(0xFF2196F3)),
      ),
      child: const Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(Icons.add, color: Color(0xFF2196F3)),
          SizedBox(width: 8),
          Text(
            'Add New Card',
            style: TextStyle(
              color: Color(0xFF2196F3),
              fontSize: 16,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}