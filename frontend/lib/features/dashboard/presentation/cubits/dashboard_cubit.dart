import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:ai_boi/core/data/operations_remote_data_source.dart';
import 'package:ai_boi/features/dashboard/data/models/dashboard_model.dart';
import 'package:ai_boi/features/dashboard/presentation/cubits/dashboard_state.dart';

class DashboardCubit extends Cubit<DashboardState> {
  final OperationsRemoteDataSource operations;

  DashboardCubit({required this.operations}) : super(DashboardInitial());

  Future<void> loadDashboard(int propertyId) async {
    emit(DashboardLoading());
    try {
      final data = await operations.getDashboard(propertyId);
      final model = DashboardModel.fromJson(data);
      emit(DashboardLoaded(model));
    } catch (e) {
      emit(DashboardError(e.toString()));
    }
  }
}
