import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

void main() {
  runApp(const ProviderScope(child: BaalavidyaApp()));
}

class BaalavidyaApp extends StatelessWidget {
  const BaalavidyaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      title: 'BAALAVIDYA',
      home: HelloScreen(),
    );
  }
}

class HelloScreen extends StatelessWidget {
  const HelloScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: Text('BAALAVIDYA')),
    );
  }
}
