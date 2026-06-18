import '../../../../core/domain/entity.dart';

class Animal extends Entity {
  const Animal({
    required int id,
    required this.identificationNumber,
    this.name,
    required this.sex,
    this.breed,
    required this.category,
    required this.lifeStatus,
    this.reproductiveStatus,
    required this.birthDate,
    required this.origin,
    this.batchId,
    this.notes,
    this.birthWeight,
    this.weaningWeight,
    this.entryDate,
    this.pedigreePo,
  }) : super(id);

  final int identificationNumber;
  final String? name;
  final String sex;
  final String? breed;
  final String category;
  final String lifeStatus;
  final String? reproductiveStatus;
  final String birthDate;
  final String origin;
  final int? batchId;
  final String? notes;
  final double? birthWeight;
  final double? weaningWeight;
  final String? entryDate;
  final int? pedigreePo;

  bool get isFemale => sex == 'F';
  bool get isActive => lifeStatus == 'ATIVO';
  bool get isDead => lifeStatus == 'MORTO' || lifeStatus == 'ABATIDO';

  String get displayName =>
      (name != null && name!.isNotEmpty) ? name! : identificationNumber.toString();

  String get sexLabel => isFemale ? 'Fêmea' : 'Macho';
}

