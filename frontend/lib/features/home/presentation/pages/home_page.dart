import 'package:ai_boi/core/di/app_bindings.dart';
import 'package:ai_boi/core/navigation/app_router.dart';
import 'package:ai_boi/core/theme/app_colors.dart';
import 'package:ai_boi/core/widgets/agrofence_shell.dart';
import 'package:ai_boi/features/registration/domain/entities/registration_draft.dart';
import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key, this.property});

  final RegisteredProperty? property;

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _scaffoldKey = GlobalKey<ScaffoldState>();
  RegisteredProperty? _property;
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _property = widget.property;
    _loadProperty();
  }

  Future<void> _loadProperty() async {
    if (_property != null) {
      if (mounted) setState(() => _loading = false);
      return;
    }
    try {
      final properties = await AppBindings.propertyRepository().listProperties();
      if (mounted) {
        setState(
          () => _property = properties.isEmpty ? null : properties.first,
        );
      }
    } finally {
      if (mounted) {
        setState(() => _loading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    final propertyName = _property?.name ?? 'Sabiá Dourado';

    return Scaffold(
      key: _scaffoldKey,
      backgroundColor: AppColors.figmaBackground,
      drawer: AgroFenceDrawer(
        propertyName: propertyName,
        currentRoute: AppRouter.home,
        onPropertySelected: (prop) => setState(() => _property = prop),
      ),
      body: SafeArea(
        child: _loading
            ? const Center(child: CircularProgressIndicator())
            : Column(
                children: [
                  AgroFenceTopBar(
                    propertyName: propertyName,
                    onMenu: () => _scaffoldKey.currentState?.openDrawer(),
                    onNotifications: () => Navigator.pushNamed(
                      context,
                      AppRouter.profile,
                      arguments: 1,
                    ),
                    onPropertySelected: (prop) =>
                        setState(() => _property = prop),
                  ),
                  const Expanded(
                    child: SizedBox.expand(),
                  ),
                ],
              ),
      ),
    );
  }
}
