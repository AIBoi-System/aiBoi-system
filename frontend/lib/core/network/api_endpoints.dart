/// Rotas da API v1 — espelham os routers do backend.
class ApiEndpoints {
  ApiEndpoints._();

  // UC01 – Proprietário / Auth (RF001, RF018)
  static const authLogin = '/auth/login';
  static const authMe = '/auth/me';
  static const authForgotPassword = '/auth/forgot-password';
  static const authResetPassword = '/auth/reset-password';
  static const authSignupSendCode = '/auth/signup/send-code';
  static const authSignupVerifyCode = '/auth/signup/verify-code';
  static const authSignupRegister = '/auth/signup/register';

  static const users = '/users/';
  static const addresses = '/addresses/';
  static const ownerModules = '/owner-modules';

  // UC02 – Propriedade (RF002, RF020)
  static const properties = '/properties/';

  // Operacional pecuária
  static const animals = '/animals/'; // RF003
  static const batches = '/batches/'; // RF004
  static const reproductions = '/reproductions/'; // RF005
  static const health = '/health/'; // RF006
  static const pastures = '/pastures/'; // RF009
  static const paddocks = '/paddocks/'; // RF008
  static const weighings = '/weighings/'; // RF024

  // RF011 – módulos habilitados por proprietário
  static String ownerModulesByOwner(int ownerId) =>
      '$ownerModules/$ownerId';

  static String propertyById(int id) => '/properties/$id';
  static String animalById(int id) => '/animals/$id';
  static String weighingsByAnimal(int animalId) =>
      '/weighings/animal/$animalId';
  static String reproductionBirth(int reproductionId) =>
      '/reproductions/$reproductionId/birth';

  static String pasturesByProperty(int propertyId) =>
      '$pastures?property_id=$propertyId';
  static String paddocksByProperty(int propertyId) =>
      '$paddocks?property_id=$propertyId';
}

