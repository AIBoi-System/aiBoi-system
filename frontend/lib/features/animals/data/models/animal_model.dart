import '../../domain/entities/animal.dart';

class AnimalModel extends Animal {
  const AnimalModel({
    required int id,
    required int identificationNumber,
    String? name,
    required String sex,
    String? breed,
    required String category,
    required String lifeStatus,
    String? reproductiveStatus,
    required String birthDate,
    required String origin,
    int? batchId,
    String? notes,
    double? birthWeight,
    double? weaningWeight,
    String? entryDate,
    int? pedigreePo,
  }) : super(
         id: id,
         identificationNumber: identificationNumber,
         name: name,
         sex: sex,
         breed: breed,
         category: category,
         lifeStatus: lifeStatus,
         reproductiveStatus: reproductiveStatus,
         birthDate: birthDate,
         origin: origin,
         batchId: batchId,
         notes: notes,
         birthWeight: birthWeight,
         weaningWeight: weaningWeight,
         entryDate: entryDate,
         pedigreePo: pedigreePo,
       );

  factory AnimalModel.fromJson(Map<String, dynamic> json) {
    return AnimalModel(
      id: json['id_animal'] as int,
      identificationNumber: json['identification_number'] as int,
      name: json['name'] as String?,
      sex: json['sex']?.toString() ?? 'F',
      breed: json['breed'] as String?,
      category: json['animal_category']?.toString() ?? '',
      lifeStatus: json['animal_life_status']?.toString() ?? 'ATIVO',
      reproductiveStatus: json['reproductive_status'] as String?,
      birthDate: json['birth_date']?.toString() ?? '',
      origin: json['origin']?.toString() ?? '',
      batchId: json['batch_id'] as int?,
      notes: json['notes'] as String?,
      birthWeight: (json['birth_weight'] as num?)?.toDouble(),
      weaningWeight: (json['weaning_weight'] as num?)?.toDouble(),
      entryDate: json['entry_date'] as String?,
      pedigreePo: json['pedigree_po'] as int?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'identification_number': identificationNumber,
      if (name != null && name!.isNotEmpty) 'name': name,
      'sex': sex,
      if (breed != null && breed!.isNotEmpty) 'breed': breed,
      'animal_size': 'MÉDIO',
      'animal_life_status': lifeStatus,
      'animal_category': category,
      'birth_date': birthDate,
      'origin': origin,
      if (isFemale && reproductiveStatus != null)
        'reproductive_status': reproductiveStatus,
      if (batchId != null) 'batch_id': batchId,
      if (notes != null && notes!.isNotEmpty) 'notes': notes,
      if (birthWeight != null) 'birth_weight': birthWeight,
      if (weaningWeight != null) 'weaning_weight': weaningWeight,
      if (entryDate != null) 'entry_date': entryDate,
      if (pedigreePo != null) 'pedigree_po': pedigreePo,
    };
  }
}
