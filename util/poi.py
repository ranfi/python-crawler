


class PoiConvert:

	MCBAND = [12890594.86, 8362377.87, 5591021, 3481989.83, 1678043.12, 0]
	MC2LL = [[1.410526172116255e-8, 0.00000898305509648872, -1.9939833816331, 200.9824383106796, -187.2403703815547,
					91.6087516669843, -23.38765649603339, 2.57121317296198, -0.03801003308653, 17337981.2],
				 [-7.435856389565537e-9, 0.000008983055097726239, -0.78625201886289, 96.32687599759846, -1.85204757529826,
					-59.36935905485877, 47.40033549296737, -16.50741931063887, 2.28786674699375, 10260144.86],
				 [-3.030883460898826e-8, 0.00000898305509983578, 0.30071316287616, 59.74293618442277, 7.357984074871,
					-25.38371002664745, 13.45380521110908, -3.29883767235584, 0.32710905363475, 6856817.37],
				 [-1.981981304930552e-8, 0.000008983055099779535, 0.03278182852591, 40.31678527705744, 0.65659298677277,
					-4.44255534477492, 0.85341911805263, 0.12923347998204, -0.04625736007561, 4482777.06 ],
				[3.09191371068437e-9, 0.000008983055096812155, 0.00006995724062, 23.10934304144901, -0.00023663490511,
					-0.6321817810242, -0.00663494467273, 0.03430082397953, -0.00466043876332, 2555164.4 ],
				[2.890871144776878e-9, 0.000008983055095805407, -3.068298e-8, 7.47137025468032, -0.00000353937994,
					-0.02145144861037, -0.00001234426596, 0.00010322952773, -0.00000323890364, 826088.5 ] ]
	lng = 0
	lat = 0

	@staticmethod
	def convertor(lng, lat):
		lat1 = abs(lat)
		ce = []
		for i in range(0, len(PoiConvert.MCBAND),1):
			if lat1 >= PoiConvert.MCBAND[i]:
				ce = PoiConvert.MC2LL[i]
				break;
		return PoiConvert._convertor(lng, lat, ce)

	@classmethod
	def _convertor(self,lng, lat, ce):
		t = ce[0] + ce[1] * abs(lng);
		cB = abs(lat) / ce[9];
		cE = ce[2] + ce[3] * cB + ce[4] * cB * cB + ce[5] * cB * cB * cB + ce[6] * cB * cB * cB * cB + ce[7]* cB * cB * cB * cB * cB + ce[8] * cB * cB * cB * cB * cB * cB;
		t *= (-1 if lng < 0 else 1);
		cE *= (-1 if lat < 0 else 1);
		return (round(t,6),round(cE,6))


if __name__=='__main__':

    
	lnglat = PoiConvert.convertor(12960169.65,4844931.00)
	lng,lat = lnglat
	print lng,lat


    
