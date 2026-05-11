import 'package:flutter/material.dart';
import 'dart:async';
import 'package:ai_boi/features/auth/presentation/pages/login_page.dart';

class WelcomePage extends StatefulWidget {
  const WelcomePage({super.key});

  @override
  State<WelcomePage> createState() => _WelcomePageState();
}

class _WelcomePageState extends State<WelcomePage> {
  // Controlador do Carrossel
  final PageController _pageController = PageController();
  int _currentPage = 0;
  Timer? _timer;
  
  final List<Map<String, String>> onboardingData = [
    {
      "title": "Controle total do rebanho",
      "subtitle": "Todos os animais organizados e acessíveis em segundos."
    },
    {
      "title": "Gestão Reprodutiva",
      "subtitle": "Acompanhe cios, prenhezes e partos com alertas inteligentes."
    },
    {
      "title": "Saúde em Dia",
      "subtitle": "Mantenha o calendário de vacinação e pesagem sob controle."
    },
    {
      "title": "Relatórios Precisos",
      "subtitle": "Tome decisões baseadas em dados reais da sua fazenda."
    },
  ];

  @override
  void initState() {
    super.initState();
    // Cria um loop infinito que roda a cada 4 segundos
    _timer = Timer.periodic(const Duration(seconds: 4), (Timer timer) {
      if (_currentPage < onboardingData.length - 1) {
        _currentPage++;
      } else {
        _currentPage = 0; // Se chegou na última, volta para a primeira
      }

      // Faz a animação de deslize suave
      if (_pageController.hasClients) {
        _pageController.animateToPage(
          _currentPage,
          duration: const Duration(milliseconds: 350),
          curve: Curves.easeInOut,
        );
      }
    });
  }


  @override
  void dispose() {
    _timer?.cancel(); // Cancela o timer para evitar vazamento de memória
    _pageController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Stack(
        children: [
          Positioned.fill(
            child: Image.asset(
              'assets/images/bg_welcome_page.jpg', 
              fit: BoxFit.cover,
            ),
          ),

          // 3. Conteúdo da Tela
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 24.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.end,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: [
                  
                  // --- ÁREA DO CARROSSEL ---
                  SizedBox(
                    height: 200, // Altura reservada para os textos
                    child: PageView.builder(
                      controller: _pageController,
                      onPageChanged: (value) {
                        setState(() {
                          _currentPage = value;
                        });
                      },
                      itemCount: onboardingData.length,
                      itemBuilder: (context, index) {
                        return Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Text(
                              onboardingData[index]["title"]!,
                              textAlign: TextAlign.center,
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 32,
                                fontWeight: FontWeight.bold,
                                fontFamily: 'Poppins',
                                height: 1.1,
                              ),
                            ),
                            const SizedBox(height: 16),
                            Text(
                              onboardingData[index]["subtitle"]!,
                              textAlign: TextAlign.center,
                              style: const TextStyle(
                                color: Colors.white70,
                                fontSize: 16,
                                fontFamily: 'Poppins',
                              ),
                            ),
                          ],
                        );
                      },
                    ),
                  ),

                  const SizedBox(height: 16),

                  // --- Indicador de Página ---
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: List.generate(
                      onboardingData.length,
                      (index) => buildDot(index: index),
                    ),
                  ),

                  const SizedBox(height: 48), // Espaço antes dos botões

                  // --- BOTÕES FIXOS ---
                  SizedBox(
                    width: double.infinity,
                    height: 56,
                    child: ElevatedButton(
                      onPressed: () {
                        // Navega para o Cadastro
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.white,
                        foregroundColor: Colors.black,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                      child: const Text(
                        'Criar uma conta',
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 16),
                  
                  Center(
                    child: TextButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => const LoginPage()),
                        );
                      },
                      child: RichText(
                        text: const TextSpan(
                          text: 'Já tem uma conta? ',
                          style: TextStyle(color: Colors.white, fontSize: 16),
                          children: [
                            TextSpan(
                              text: 'Entrar',
                              style: TextStyle(
                                fontWeight: FontWeight.bold,
                                decoration: TextDecoration.underline,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  // Função que desenha cada bolinha
  Widget buildDot({required int index}) {
    return AnimatedContainer(
      duration: const Duration(milliseconds: 200),
      margin: const EdgeInsets.only(right: 8),
      height: 8,
      // Se for a página atual, a bolinha fica maior e totalmente branca
      width: _currentPage == index ? 24 : 8,
      decoration: BoxDecoration(
        color: _currentPage == index ? Colors.white : Colors.white.withValues(alpha: 0.4),
        borderRadius: BorderRadius.circular(4),
      ),
    );
  }
}