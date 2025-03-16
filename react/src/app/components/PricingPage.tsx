import React from 'react';
import { Check } from 'lucide-react';

function PricingTier({ 
  name, 
  price, 
  description, 
  features, 
  highlighted = false 
}: { 
  name: string;
  price: string;
  description: string;
  features: string[];
  highlighted?: boolean;
}) {
  return (
    <div className={`rounded-2xl p-8 ${
      highlighted 
        ? 'bg-blue-600 text-white shadow-xl scale-105' 
        : 'bg-white text-gray-900'
    }`}>
      <h3 className="text-2xl font-bold">{name}</h3>
      <p className={`mt-4 text-sm ${highlighted ? 'text-blue-100' : 'text-gray-500'}`}>
        {description}
      </p>
      <div className="mt-6">
        <span className="text-4xl font-bold">{price}</span>
        {price !== 'Grátis' && <span className={`${highlighted ? 'text-blue-100' : 'text-gray-500'}`}>/mês</span>}
      </div>
      <ul className="mt-8 space-y-4">
        {features.map((feature, index) => (
          <li key={index} className="flex items-center gap-3">
            <Check className={`h-5 w-5 ${
              highlighted ? 'text-blue-200' : 'text-blue-600'
            }`} />
            <span className="text-sm">{feature}</span>
          </li>
        ))}
      </ul>
      <button className={`mt-8 w-full rounded-lg py-3 px-6 text-center font-semibold transition-all ${
        highlighted
          ? 'bg-white text-blue-600 hover:bg-blue-50'
          : 'bg-blue-600 text-white hover:bg-blue-700'
      }`}>
        Começar
      </button>
    </div>
  );
}

function PricingPage() {
  const pricingTiers = [
    {
      name: "Grátis",
      price: "Grátis",
      description: "Perfeito para projetos pessoais e aplicações simples",
      features: [
        "Até 1.000 chamadas de API/mês",
        "Análises básicas",
        "Suporte da comunidade",
        "1 membro da equipe",
        "Documentação básica"
      ]
    },
    {
      name: "Básico",
      price: "R$149",
      description: "Ótimo para empresas e equipes em crescimento",
      features: [
        "Até 50.000 chamadas de API/mês",
        "Análises avançadas",
        "Suporte prioritário por e-mail",
        "5 membros da equipe",
        "Documentação avançada",
        "Integrações personalizadas"
      ],
      highlighted: true
    },
    {
      name: "Pro",
      price: "R$499",
      description: "Para empresas e aplicações de grande escala",
      features: [
        "Chamadas de API ilimitadas",
        "Análises em tempo real",
        "Suporte telefônico 24/7",
        "Membros da equipe ilimitados",
        "Soluções personalizadas",
        "Gerente de conta dedicado",
        "Garantia de SLA"
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-24 sm:px-6 lg:px-8">
        <div className="text-center">
          <h2 className="text-base font-semibold text-blue-600">Preços</h2>
          <p className="mt-2 text-4xl font-bold tracking-tight text-gray-900">
            Escolha o plano certo para você
          </p>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-500">
            Preços simples e transparentes que crescem com o seu negócio. Sem taxas ocultas ou cobranças surpresa.
          </p>
        </div>

        <div className="mt-20 grid grid-cols-1 gap-8 md:grid-cols-3">
          {pricingTiers.map((tier, index) => (
            <PricingTier key={index} {...tier} />
          ))}
        </div>
      </div>
    </div>
  );
}

export default PricingPage;