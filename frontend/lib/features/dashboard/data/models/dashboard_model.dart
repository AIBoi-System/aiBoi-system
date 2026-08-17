class DashboardModel {
  final int propertyId;
  final String propertyName;
  final int totalAnimals;
  final int totalPastures;
  final int totalPaddocks;
  final int totalBatches;
  final List<RecentWeighing> recentWeighings;
  final List<RecentHealthRecord> recentHealthRecords;

  DashboardModel({
    required this.propertyId,
    required this.propertyName,
    required this.totalAnimals,
    required this.totalPastures,
    required this.totalPaddocks,
    required this.totalBatches,
    required this.recentWeighings,
    required this.recentHealthRecords,
  });

  factory DashboardModel.fromJson(Map<String, dynamic> json) {
    return DashboardModel(
      propertyId: json['property_id'] as int,
      propertyName: json['property_name'] as String,
      totalAnimals: json['total_animals'] as int,
      totalPastures: json['total_pastures'] as int,
      totalPaddocks: json['total_paddocks'] as int,
      totalBatches: json['total_batches'] as int,
      recentWeighings: (json['recent_weighings'] as List? ?? [])
          .map((e) => RecentWeighing.fromJson(e as Map<String, dynamic>))
          .toList(),
      recentHealthRecords: (json['recent_health_records'] as List? ?? [])
          .map((e) => RecentHealthRecord.fromJson(e as Map<String, dynamic>))
          .toList(),
    );
  }
}

class RecentWeighing {
  final int id;
  final double weight;
  final String weighDate;
  final int animalId;
  final int animalIdentification;

  RecentWeighing({
    required this.id,
    required this.weight,
    required this.weighDate,
    required this.animalId,
    required this.animalIdentification,
  });

  factory RecentWeighing.fromJson(Map<String, dynamic> json) {
    return RecentWeighing(
      id: json['id'] as int,
      weight: (json['weight'] as num).toDouble(),
      weighDate: json['weigh_date'] as String,
      animalId: json['animal_id'] as int,
      animalIdentification: json['animal_identification'] as int,
    );
  }
}

class RecentHealthRecord {
  final int idHealthRecord;
  final String healthType;
  final String productName;
  final String applicationDate;
  final String? responsible;
  final int? animalId;

  RecentHealthRecord({
    required this.idHealthRecord,
    required this.healthType,
    required this.productName,
    required this.applicationDate,
    this.responsible,
    this.animalId,
  });

  factory RecentHealthRecord.fromJson(Map<String, dynamic> json) {
    return RecentHealthRecord(
      idHealthRecord: json['id_health_record'] as int,
      healthType: json['health_type'] as String,
      productName: json['product_name'] as String,
      applicationDate: json['application_date'] as String,
      responsible: json['responsible'] as String?,
      animalId: json['animal_id'] as int?,
    );
  }
}
